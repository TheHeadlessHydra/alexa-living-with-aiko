"""
Main entrypoint. Routes the request via a state machine. 
"""

from __future__ import print_function

from state_machine_launch import *
from state_machine_common import *
from in_skill_purchase import *

from ask_sdk_core.api_client import DefaultApiClient
from ask_sdk_core.attributes_manager import AttributesManager, AbstractPersistenceAdapter
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.serialize import DefaultSerializer
from ask_sdk_model import RequestEnvelope
from ask_sdk_model.services import ApiConfiguration, ServiceClientFactory


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest, etc.)
    Old state is recovered via the session field. If no state, it can be assumed this is an initialize state. 
    The request type or intent name is the "input" or "action" that is given to the state machine.
    """

    if event['session']['application']['applicationId'] != "amzn1.ask.skill.bda58b10-daf5-420c-be9b-f699ae652105":
        raise ValueError("Invalid Application ID")

    handler_input = get_handler_input(event, context)

    override_source = None
    if event['request']['type'] == "LaunchRequest":
        input_action = "LaunchRequest"
    elif event['request']['type'] == "IntentRequest":
        input_action = event['request']['intent']['name']
    elif event['request']['type'] == "SessionEndedRequest":
        input_action = "SessionEndedRequest"
    elif event['request']['type'] == "Connections.Response":
        print(event)
        send_request_target = event['request']['name']  # one of Upsell, Buy or Cancel
        purchase_result = event['request']['payload']['purchaseResult']  # ACCEPTED, DECLINED, ALREADY_PURCHASED, ERROR
        product_id = event['request']['payload']['productId']
        input_action = purchase_result
        override_source = get_directive_action_mapping(send_request_target, product_id)
    else:
        raise ValueError("Unknown request type")

    input_action = clean_intent_action(input_action)
    storage = get_storage_layer(Config.storage_layer)

    print("======= STARTING STATE MACHINE PROCESS WITH: " + input_action)

    # If this is an initial state, it will be called with the same input action that was used to build it. This is fine. 
    print(input_action)
    print(event)
    state_machine = get_state_machine_from_session(
        event['session'], input_action, storage, handler_input, override_source)
    decorate_and_validate_session_is_purchased(handler_input, state_machine.session)

    print("state_machine: {}".format(state_machine))

    return_object = state_machine.next(input_action, handler_input)

    session = state_machine.get_session()
    session.set_total_number_of_utterances(session.get_total_number_of_utterances() + 1)
    save_game(session, storage)

    print(return_object)
    with_upsell = upsell_return_object(return_object, handler_input, session)
    print(with_upsell)

    return with_upsell


def clean_intent_action(intent_action):
    if intent_action.startswith("AMAZON."):
        return intent_action.replace("AMAZON.", "")
    else:
        return intent_action


def get_state_machine_from_session(alexa_session, input_action, storage, handler_input, override_source=None):
    """ If there is a state in the session, recover it.
    If there is no state in the session, try to recover it from storage.
    If there is no session state in storage, start a new session.
    If this is a STOP intent, write the session state out to storage.
    override_source tells the state machine to start from a specific state
    """

    if 'user' not in alexa_session and 'userId' not in alexa_session['user']:
        raise ValidationException("Could not get user id from session object")
    user_id = alexa_session['user']['userId']

    if 'attributes' not in alexa_session or alexa_session['attributes'] is None:
        print("No session state found in request. Searching table for stored state")
        session_state_json_string = storage.get_json_string(user_id)

        if session_state_json_string is None:
            print("No session state found. Starting from scratch")
            # supersede if certain intents are called. End session and write state to storage.
            state_machine = supersede_build_state_machine(input_action, Session(SessionState(user_id)), handler_input)
            if state_machine is not None:
                return state_machine

            if override_source is None:
                return initialize_new_state_machine_from_input(input_action, user_id=user_id)
            else:
                return build_state_machine_from_source(override_source, user_id=user_id)

    else:
        session_state_json_string = alexa_session['attributes']

    print(session_state_json_string)

    try:
        print("Converting session_state_json into Session object")
        session = json_string_to_session(session_state_json_string)

        # supersede if certain intents are called. End session and write state to storage.
        state_machine = supersede_build_state_machine(input_action, session, handler_input)
        if state_machine is not None:
            return state_machine

        if override_source is None:
            return rebuild_state_machine_from_session(input_action, session)
        else:
            return build_state_machine_from_source(override_source, session=session)
    except ValidationException:
        message = "Invalid state stored: " + str(session_state_json_string)
        print(message)
        raise CannotBuildStateMachineException(message)


def supersede_build_state_machine(input_action, session, handler_input):
    if input_action == STOP_INTENT or input_action == CANCEL_INTENT or input_action == SESSION_ENDED:
        return initialize_new_stop_game(session)
    elif input_action == HELP_INTENT:
        return initialize_new_help_game(session)

    return None


def save_game(session, storage):
    user_id = session.get_user_id_serializable()
    session_string = session_to_json_string(session)
    storage.write_json_string(user_id, session_string)


def get_handler_input(event, context):
    serializer = DefaultSerializer()
    request_envelope = serializer.deserialize(payload=json.dumps(event), obj_type=RequestEnvelope)
    api_client = DefaultApiClient()
    api_token = request_envelope.context.system.api_access_token
    api_endpoint = request_envelope.context.system.api_endpoint

    api_configuration = ApiConfiguration(
        serializer=serializer, api_client=api_client,
        authorization_value=api_token,
        api_endpoint=api_endpoint)
    factory = ServiceClientFactory(api_configuration=api_configuration)

    attributes_manager = AttributesManager(
        request_envelope=request_envelope,
        persistence_adapter=AbstractPersistenceAdapter())

    handler_input = HandlerInput(
        request_envelope=request_envelope,
        attributes_manager=attributes_manager,
        context=context,
        service_client_factory=factory)

    return handler_input


def get_directive_action_mapping(send_request_target, product_id):
    if send_request_target == "Upsell":
        if product_id == TSUNDERE_MODE_PRODUCT_ID:
            return "DirectiveResponseBuyTsundereMode"
        elif product_id == CAFE_DATE_PRODUCT_ID:
            return "DirectiveResponseBuyCafeDate"
        else:
            raise Exception("Unknown product id: {}".format(product_id))
    elif send_request_target == "Buy":
        if product_id == TSUNDERE_MODE_PRODUCT_ID:
            return "DirectiveResponseBuyTsundereMode"
        elif product_id == CAFE_DATE_PRODUCT_ID:
            return "DirectiveResponseBuyCafeDate"
        else:
            raise Exception("Unknown product id: {}".format(product_id))
    elif send_request_target == "Cancel":
        if product_id == TSUNDERE_MODE_PRODUCT_ID:
            return "DirectiveResponseCancelTsundereMode"
        elif product_id == CAFE_DATE_PRODUCT_ID:
            return "DirectiveResponseCancelCafeDate"
        else:
            raise Exception("Unknown product id: {}".format(product_id))
    else:
        raise Exception("Unknown send_request_target id: {}".format(send_request_target))

# --------------- Main used for testing ------------------


def build_fake_lambda_event(request_type, intent_name, existing_session, attributes=None):
    if existing_session:
        if attributes is not None:
            return {"request": {"type": request_type, "intent": {"name": intent_name}},
                    "session": {
                        "application": {"applicationId": "amzn1.ask.skill.bda58b10-daf5-420c-be9b-f699ae652105"},
                        "user": {
                            "userId": "amzn1.ask.account.AE3O74TXA4Z4TEYVFDVBQ74CIHE7QBXXLPHDNBDFRWDIXPKB5MRRTZ47QNMYD7UY2ZFNJJNCWD4G2B362IZMUZ6XEAGE3YCHNVD5GFQTUIEN23GOW3AO5BHUAU5R37Y7GZ6F7YGNQEIYKZT7GFSTMLNJ237T3NY7KBA3GMW3G7YX5RKRXE2UA3YZGEYOMEXHRZZ6RLVMBX427BY"},
                        "attributes": attributes
                        }}
        else:
            return {"request": {"type": request_type, "intent": {"name": intent_name}},
                    "session": {
                        "application": {"applicationId": "amzn1.ask.skill.bda58b10-daf5-420c-be9b-f699ae652105"},
                        "user": {
                            "userId": "amzn1.ask.account.AE3O74TXA4Z4TEYVFDVBQ74CIHE7QBXXLPHDNBDFRWDIXPKB5MRRTZ47QNMYD7UY2ZFNJJNCWD4G2B362IZMUZ6XEAGE3YCHNVD5GFQTUIEN23GOW3AO5BHUAU5R37Y7GZ6F7YGNQEIYKZT7GFSTMLNJ237T3NY7KBA3GMW3G7YX5RKRXE2UA3YZGEYOMEXHRZZ6RLVMBX427BY"}
                        }}
    else:
        return {"request": {"type": request_type, "intent": {"name": intent_name}},
                "session": {"application": {"applicationId": "amzn1.ask.skill.bda58b10-daf5-420c-be9b-f699ae652105"},
                            "user": {
                                "userId": "amzn1.ask.account.AE3O74TXA4Z4TEYVFDVBQ74CIHE7QBXXLPHDNBDFRWDIXPKB5MRRTZ47QNMYD7UY2ZFNJJNCWD4G2B362IZMUZ6XEAGE3YCHNVD5GFQTUIEN23GOW3AO5BHUAU5R37Y7GZ6F7YGNQEIYKZT7GFSTMLNJ237T3NY7KBA3GMW3G7YX5RKRXE2UA3YZGEYOMEXHRZZ6RLVMBX427BY"}}}


if __name__ == "__main__":
    # set and follow
    event = build_fake_lambda_event("LaunchRequest", "", False)
    #event = build_fake_lambda_event("IntentRequest", "InitializeBuyTsundereMode", True)

    # initalization
    #event = build_fake_lambda_event("IntentRequest", "InitializeWhatIsAikoThinking", True)
    return_body = lambda_handler(event, None)
    print(return_body)
