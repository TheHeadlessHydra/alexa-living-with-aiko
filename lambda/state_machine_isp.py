from state import State
from state_machine_at_home import CommandSwitchToTsundereMode
from state_machine_helpers import *
from sound_mappings_isp import *
from state_machine_common import *
from in_skill_purchase import *
from ask_sdk_model.services.monetization.entitlement_reason import EntitlementReason


class InitializeWhatCanBePurchased(State):
    def next(self, input_action, session, handler_input):
        card_title = "What can be bought"

        cafe_date_purchasable = is_product_purchasable(handler_input, ProductName.CAFE_DATE)
        tsundere_mode_purchasable = is_product_purchasable(handler_input, ProductName.TSUNDERE_MODE)
        print(str(cafe_date_purchasable))
        print(str(tsundere_mode_purchasable))

        if cafe_date_purchasable and tsundere_mode_purchasable:
            # TODO: both can be purchased... need special line here
            speech_output = wrap_with_speak("You can buy the Tsundere voice pack and a date at the cafe.")
        elif cafe_date_purchasable and not tsundere_mode_purchasable:
            # TODO: date purchaseable but not tsundere mode
            speech_output = wrap_with_speak("You can buy the cafe date pack.")
        elif not cafe_date_purchasable and tsundere_mode_purchasable:
            speech_output = wrap_with_speak(random_build_audio_arrays([WHAT_CAN_BE_PURCHASED_TSUNDERE_MODE]))
        else:
            # TODO: neither is purchaseable?
            speech_output = wrap_with_speak("Nothing can be purchased at the moment.")

        reprompt_text = wrap_with_speak("Is there anything else you want to say to Aiko Chan?")
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class InitializeWhatsBeenPurchased(State):
    def next(self, input_action, session, handler_input):
        card_title = "What can be bought"

        cafe_date_purchased = is_product_purchased(handler_input, ProductName.CAFE_DATE)
        tsundere_mode_purchased = is_product_purchased(handler_input, ProductName.TSUNDERE_MODE)

        if cafe_date_purchased and tsundere_mode_purchased:
            speech_output = wrap_with_speak(random_build_audio_arrays([WHAT_BUY_TSUNDERE_AND_DATE]))
        elif cafe_date_purchased and not tsundere_mode_purchased:
            speech_output = wrap_with_speak(random_build_audio_arrays([WHAT_BUY_CAFE_DATE]))
        elif not cafe_date_purchased and tsundere_mode_purchased:
            speech_output = wrap_with_speak(random_build_audio_arrays([WHAT_BUY_TSUNDERE_MODE]))
        else:
            # TODO: missing neither bought
            speech_output = wrap_with_speak("You have not purchased either the Tsundere voice mode or the Cafe Date.")

        reprompt_text = wrap_with_speak("Is there anything else you want to say to Aiko Chan?")
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class InitializeMoreAboutDate(State):
    def next(self, input_action, session, handler_input):
        card_title = "What can be bought"
        speech_output = wrap_with_speak(
            random_build_audio_arrays(
                [DATE_DESCRIPTION]
            ))
        reprompt_text = wrap_with_speak("Is there anything else you want to say to Aiko Chan?")
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class InitializeMoreAboutTsundereMode(State):
    def next(self, input_action, session, handler_input):
        card_title = "What can be bought"
        speech_output = wrap_with_speak(
            random_build_audio_arrays(
                [TSUNDERE_DESCRIPTION]
            ))
        reprompt_text = wrap_with_speak("Is there anything else you want to say to Aiko Chan?")
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class InitializeWhatsFreeVsPaid(State):
    def next(self, input_action, session, handler_input):
        card_title = "What can be bought"
        speech_output = wrap_with_speak(
            random_build_audio_arrays(
                [FREE_VS_PAID]
            ))
        reprompt_text = wrap_with_speak("Is there anything else you want to say to Aiko Chan?")
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class InitializeBuyTsundereMode(State):
    def next(self, input_action, session, handler_input):
        card_title = "Buy tsundere mode"
        product_id = get_product_id(handler_input, ProductName.TSUNDERE_MODE)

        if product_id is not None:
            speech_output = wrap_with_speak("")
            reprompt_text = wrap_with_speak("")
            should_end_session = True
            session.set_stored_game_state(None)
            return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session,
                                       buy_product_id=product_id)
        else:
            speech_output = wrap_with_speak(
                "I am sorry. That product is not available for purchase."
            )
            reprompt_text = wrap_with_speak("Is there anything else you want to say to Aiko Chan?")
            should_end_session = False
            session.set_stored_game_state(None)
            return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class InitializeReturnTsundereMode(State):
    def next(self, input_action, session, handler_input):
        card_title = "Return tsundere mode"
        product_id = get_product_id(handler_input, ProductName.TSUNDERE_MODE)

        if product_id is not None:
            speech_output = wrap_with_speak("")
            reprompt_text = wrap_with_speak("")
            should_end_session = True
            session.set_stored_game_state(None)
            return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session,
                                       cancel_product_id=product_id)
        else:
            speech_output = wrap_with_speak(
                "You have not purchased tsundere mode. It does not need to be returned."
            )
            reprompt_text = wrap_with_speak("Is there anything else you want to say to Aiko Chan?")
            should_end_session = False
            session.set_stored_game_state(None)
            return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class InitializeBuyCafeDate(State):
    def next(self, input_action, session, handler_input):
        card_title = "Buy cafe date"
        product_id = get_product_id(handler_input, ProductName.CAFE_DATE)

        if product_id is not None:
            speech_output = wrap_with_speak("")
            reprompt_text = wrap_with_speak("")
            should_end_session = True
            session.set_stored_game_state(None)
            return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session,
                                       buy_product_id=product_id)
        else:
            speech_output = wrap_with_speak(
                "I am sorry. That product is not available for purchase."
            )
            reprompt_text = wrap_with_speak("Is there anything else you want to say to Aiko Chan?")
            should_end_session = False
            session.set_stored_game_state(None)
            return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class InitializeReturnCafeDate(State):
    def next(self, input_action, session, handler_input):
        card_title = "Return cafe date"
        product_id = get_product_id(handler_input, ProductName.CAFE_DATE)

        if product_id is not None:
            speech_output = wrap_with_speak("")
            reprompt_text = ""
            should_end_session = True
            session.set_stored_game_state(None)
            return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session,
                                       cancel_product_id=product_id)
        else:
            speech_output = wrap_with_speak(
                "You have not purchased the cafe date. It does not need to be returned."
            )
            reprompt_text = wrap_with_speak("Is there anything else you want to say to Aiko Chan?")
            should_end_session = False
            session.set_stored_game_state(None)
            return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class DirectiveResponseBuyTsundereMode(State):
    def next(self, input_action, session, handler_input):
        card_title = "Buying tsundere mode."

        if input_action == "ACCEPTED":
            return CommandSwitchToTsundereMode().next(input_action, session, handler_input)
        elif input_action == "ALREADY_PURCHASED":
            speech_output = wrap_with_speak(
                random_build_audio_arrays(
                    [ALREADY_PURCHASED_TSUNDERE]
                ))
        elif input_action == "DECLINED":
            speech_output = wrap_with_speak(wrap_with_audio(ASK_FOR_REFUND_TSUNDERE))
        else:
            speech_output = wrap_with_speak(
                random_build_audio_arrays(
                    [WELCOME_BACK_1], [WELCOME_BACK_2], [WELCOME_BACK_3], [WELCOME_BACK_4], [WELCOME_BACK_5]
                ))

        reprompt_text = wrap_with_speak("Is there anything else you want to say to Aiko Chan?")
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class DirectiveResponseCancelTsundereMode(State):
    def next(self, input_action, session, handler_input):
        card_title = "Refund tsundere mode."

        if input_action == "ACCEPTED":
            speech_output = wrap_with_speak(wrap_with_audio(ASK_FOR_REFUND_TSUNDERE))
        elif input_action == "ALREADY_PURCHASED":
            speech_output = wrap_with_speak(
                random_build_audio_arrays(
                    [ALREADY_PURCHASED_TSUNDERE]
                ))
        else:
            speech_output = wrap_with_speak(
                random_build_audio_arrays(
                    [WELCOME_BACK_1], [WELCOME_BACK_2], [WELCOME_BACK_3], [WELCOME_BACK_4], [WELCOME_BACK_5]
                ))

        reprompt_text = wrap_with_speak("Is there anything else you want to say to Aiko Chan?")
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)

class DirectiveResponseBuyCafeDate(State):
    def next(self, input_action, session, handler_input):
        card_title = "Buying the cafe date."

        if input_action == "ACCEPTED":
            speech_output = wrap_with_speak(
                random_build_audio_arrays(
                    [DATE_PURCHASED], [DATE_PURCHASED_ALT]
                ))
        elif input_action == "ALREADY_PURCHASED":
            speech_output = wrap_with_speak(
                random_build_audio_arrays(
                    [ALREADY_PURCHASED_DATE]
                ))
        elif input_action == "DECLINED":
            speech_output = wrap_with_speak(wrap_with_audio(ASK_FOR_REFUND_DATE))
        else:
            speech_output = wrap_with_speak(
                random_build_audio_arrays(
                    [WELCOME_BACK_1], [WELCOME_BACK_2], [WELCOME_BACK_3], [WELCOME_BACK_4], [WELCOME_BACK_5]
                ))

        reprompt_text = wrap_with_speak("Is there anything else you want to say to Aiko Chan?")
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class DirectiveResponseCancelCafeDate(State):
    def next(self, input_action, session, handler_input):
        card_title = "Refund the cafe date."

        if input_action == "ACCEPTED":
            speech_output = wrap_with_speak(wrap_with_audio(ASK_FOR_REFUND_DATE))
        elif input_action == "ALREADY_PURCHASED":
            speech_output = wrap_with_speak(
                random_build_audio_arrays(
                    [ALREADY_PURCHASED_DATE]
                ))
        else:
            speech_output = wrap_with_speak(
                random_build_audio_arrays(
                    [WELCOME_BACK_1], [WELCOME_BACK_2], [WELCOME_BACK_3], [WELCOME_BACK_4], [WELCOME_BACK_5]
                ))

        reprompt_text = wrap_with_speak("Is there anything else you want to say to Aiko Chan?")
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)
