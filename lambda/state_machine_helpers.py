"""
All helper methods to interact with the Alexa JSON object model.
"""

# --------------- Special input types ------------------
from session_state_builder import *
from storage_factory import *
from session_state_builder import *
import random
import uuid

INITIALIZE = "Initialize"
RETURN = "Return"

# --------------- Amazon intents ------------------

SESSION_ENDED = "SessionEndedRequest"
STOP_INTENT = "StopIntent"
CANCEL_INTENT = "CancelIntent"
HELP_INTENT = "HelpIntent"

# --------------- Follow ups ------------------

FOLLOW_UP_IM_GOOD = "InitializeUserGoodDay"
FOLLOW_UP_IM_BAD = "InitializeUserBadDay"
FOLLOW_UP_ANGRY = "InitializeUserIsAngry"
FOLLOW_UP_TIRED = "InitializeUserIsTired"


# --------------- helpers for the game ------------------

def save_game(session):
    storage = get_storage_layer(Config.storage_layer)
    session_string = session_to_json_string(session)
    storage.write_json_string(session.get_user_id_serializable(), session_string)

# --------------- builders ------------------


def get_action_response(session, card_title, speech_output, reprompt_text, should_end_session, buy_product_id=None,
                        cancel_product_id=None):
    session_state_json = session_to_json_string(session)
    return build_response(session_state_json, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session, buy_product_id, cancel_product_id))


def build_speechlet_response(title,
                             output,
                             reprompt_text,
                             should_end_session,
                             buy_product_id=None, cancel_product_id=None):
    output_json = {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': output
        },
        'card': {
            'type': 'Simple',
            'title': title
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }
    if buy_product_id is not None:
        output_json['directives'] = [
            {
                "type": "Connections.SendRequest",
                "name": "Buy",
                "payload": {
                    "InSkillProduct": {
                        "productId": buy_product_id
                    }
                },
                "token": "correlationToken"
            }
        ]
    if cancel_product_id is not None:
        output_json['directives'] = [
            {
                "type": "Connections.SendRequest",
                "name": "Cancel",
                "payload": {
                    "InSkillProduct": {
                        "productId": cancel_product_id
                    }
                },
                "token": "correlationToken"
            }
        ]
    return output_json


def add_upsell_to_output(output_json, upsell_product_id, upsell_message):
    output_json['response']['shouldEndSession'] = True
    output_json['response']['directives'] = [
        {
            "type": "Connections.SendRequest",
            "name": "Upsell",
            "payload": {
                "InSkillProduct": {
                    "productId": upsell_product_id
                },
                "upsellMessage": upsell_message
            },
            "token": str(uuid.uuid1())
        }
    ]
    return output_json


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


class ValidationException(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(ValidationException, self).__init__(message)


# --------------- Helper methods ------------------

def random_audio(*arg):
    """ given a set of choices, will randomly choose one and return it
    """
    length = len(arg)
    random_choice_index = random.randrange(0, length)
    return arg[random_choice_index]


def random_build_audio(*arg):
    """ given a set of choices, will randomly choose one and return it with audo wrappings
    """
    random_choice = random_audio(*arg)
    return wrap_with_audio(random_choice)


def random_build_audio_arrays(*arg):
    """ Given various arrays of choices, will randomly choose one array and list
    out the choices within the array with audio wrappings.
    """
    length = len(arg)
    random_choice_index = random.randrange(0, length)
    random_choice = arg[random_choice_index]
    final_string = ""
    for choice in random_choice:
        final_string = final_string + wrap_with_audio(choice)
    return final_string


def wrap_with_speak(*arg):
    full_final_string = "<speak>"
    for a in arg:
        full_final_string = full_final_string + a
    full_final_string = full_final_string + "</speak>"
    return full_final_string


def wrap_with_audio(text):
    return "<audio src='" + text + "'/>"
