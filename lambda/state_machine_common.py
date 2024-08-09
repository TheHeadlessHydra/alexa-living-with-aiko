"""
All states that can be transitioned to from a level.
"""
from game import *
from state import State
from state_machine_helpers import *
from sound_mappings_dere import *
from sound_mappings_original import *
from sound_mappings_tsundere import *
from sound_mappings_cafe_date import *
from in_skill_purchase import TSUNDERE_MODE_PRODUCT_ID


class SessionEndedRequest(State):
    def next(self, input_action, session, handler_input):
        card_title = "I'm off!"
        if session.get_is_in_cafe_date():
            speech_output = wrap_with_speak(
                random_build_audio(CAFE_DATE_STOP_1, CAFE_DATE_STOP_2, CAFE_DATE_STOP_3, CAFE_DATE_STOP_4)
            )
            session.set_is_in_cafe_date(False)
        elif session.get_voice_mode() is VoiceMode.ORIGINAL:
            speech_output = wrap_with_speak(
                random_build_audio(
                    ORIGINAL_ITEKIMASU,
                    ORIGINAL_SEE_YOU_LATER,
                    ORIGINAL_ILL_SEE_YOU_AGAIN,
                    ORIGINAL_SAYOUNARA_HAPPY,
                    ORIGINAL_SAYOUNARA_SAD))
        elif session.get_voice_mode() is VoiceMode.DERE:
            speech_output = wrap_with_speak(
                random_build_audio(ITEKIMASU, SEE_YOU_LATER, ILL_SEE_YOU_AGAIN, SAYOUNARA_HAPPY, SAYOUNARA_SAD))
        elif session.get_voice_mode() is VoiceMode.TSUNDERE:
            speech_output = wrap_with_speak(
                random_build_audio(
                    TSUNDERE_TURN_OFF_1,
                    TSUNDERE_TURN_OFF_2))
        else:
            raise Exception("Invalid voice mode")
        reprompt_text = ""
        should_end_session = True
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class StopIntent(State):
    def next(self, input_action, session, handler_input):
        return SessionEndedRequest().next(input_action, session)


class CancelIntent(State):
    def next(self, input_action, session, handler_input):
        return SessionEndedRequest().next(input_action, session)


class HelpIntent(State):
    def next(self, input_action, session, handler_input):
        card_title = "Help"
        if session.get_is_in_cafe_date():
            speech_output = wrap_with_speak(
                random_build_audio(CAFE_DATE_HELP_1, CAFE_DATE_HELP_1),
                random_build_audio(
                    CAFE_DATE_QUESTIONS_TO_ASK_1,
                    CAFE_DATE_QUESTIONS_TO_ASK_2,
                    CAFE_DATE_QUESTIONS_TO_ASK_3,
                    CAFE_DATE_QUESTIONS_TO_ASK_4,
                    CAFE_DATE_QUESTIONS_TO_ASK_5,
                    CAFE_DATE_QUESTIONS_TO_ASK_6,
                    CAFE_DATE_QUESTIONS_TO_ASK_7,
                    CAFE_DATE_QUESTIONS_TO_ASK_8,
                    CAFE_DATE_QUESTIONS_TO_ASK_9,
                    CAFE_DATE_QUESTIONS_TO_ASK_10,
                    CAFE_DATE_QUESTIONS_TO_ASK_11
                )
            )
            reprompt_text = wrap_with_speak(
                random_build_audio(CAFE_DATE_REPROMPT_1, CAFE_DATE_REPROMPT_2)
            )
            should_end_session = False
        else:
            speech_output = wrap_with_speak(
                "If you want to interact with Aiko chan, you just need to talk to her. "
                "You can say something like <break time=\"1s\"/>" + get_questions_you_can_ask() + ". "
                "What would you like to say to Aiko chan?")
            reprompt_text = wrap_with_speak("Is there anything else you want to say to Aiko Chan?")
            should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)

# --------------- Commands ------------------


class CommandSwitchToTsundereMode(State):
    def next(self, input_action, session, handler_input):
        card_title = "Switch to Tsundere mode!"

        if not session.get_is_tsundere_mode_purchased() and session.get_is_tsundere_mode_purchasable():
            speech_output = wrap_with_speak("")
            reprompt_text = ""
            should_end_session = True
            return_object = get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)
            return add_upsell_to_output(return_object, TSUNDERE_MODE_PRODUCT_ID,
                                        "Tsundere mode is not available right now. Would you like to hear more?")
        elif not session.get_is_tsundere_mode_purchased() and not session.get_is_tsundere_mode_purchasable():
            speech_output = wrap_with_speak("We are sorry, but tsundere mode is not enabled or purchasable in your region.")
        else:
            speech_output = wrap_with_speak(
                random_build_audio_arrays(
                    [TSUNDERE_SWITCH_1], [TSUNDERE_SWITCH_2]
                ))
            session.set_voice_mode(VoiceMode.TSUNDERE)
        reprompt_text = wrap_with_speak("Is there anything else you want to say to Aiko Chan?")
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class CommandSwitchToDereMode(State):
    def next(self, input_action, session, handler_input):
        card_title = "Switch to Dere mode!"
        if session.get_voice_mode() == VoiceMode.TSUNDERE:
            speech_output = wrap_with_speak(
                random_build_audio(TSUNDERE_LEAVE_MODE_1))
        else:
            speech_output = wrap_with_speak(
                random_build_audio(MY_NAME_IS_AIKO))
        reprompt_text = wrap_with_speak("Is there anything else you want to say to Aiko Chan?")
        should_end_session = False
        session.set_stored_game_state(None)
        session.set_voice_mode(VoiceMode.DERE)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class CommandSwitchToOriginalVoice(State):
    def next(self, input_action, session, handler_input):
        card_title = "Switch to the original voice!"
        speech_output = wrap_with_speak(
            random_build_audio(ORIGINAL_MY_NAME_IS_AIKO))
        reprompt_text = wrap_with_speak("Is there anything else you want to say to Aiko Chan?")
        should_end_session = False
        session.set_stored_game_state(None)
        session.set_voice_mode(VoiceMode.ORIGINAL)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class NotUnderstood(State):
    def next(self, input_action, session, handler_input):
        card_title = "I didn't understand."
        if session.get_voice_mode() is VoiceMode.ORIGINAL:
            speech_output = wrap_with_speak(
                random_build_audio_arrays(
                    [ORIGINAL_WAKARIMASEN_DESU],
                    [ORIGINAL_AH_IM_SORRY, ORIGINAL_I_DID_NOT_UNDERSTAND],
                    [ORIGINAL_GOMEN_NE, ORIGINAL_I_DID_NOT_UNDERSTAND],
                    [ORIGINAL_IM_SORRY_DID_NOT_UNDERSTAND]
                ))
        elif session.get_voice_mode() is VoiceMode.DERE:
            speech_output = wrap_with_speak(
                random_build_audio_arrays(
                    [WAKARIMASEN_DESU],
                    [AH_IM_SORRY, I_DID_NOT_UNDERSTAND],
                    [GOMEN_NE, I_DID_NOT_UNDERSTAND],
                    [IM_SORRY_DID_NOT_UNDERSTAND]
                ))
        elif session.get_voice_mode() is VoiceMode.TSUNDERE:
            speech_output = wrap_with_speak(random_build_audio(
                TSUNDERE_DIDNT_UNDERSTAND_1,
                TSUNDERE_DIDNT_UNDERSTAND_2,
                TSUNDERE_DIDNT_UNDERSTAND_3))
        else:
            raise Exception("Invalid voice mode")
        reprompt_text = wrap_with_speak("Is there anything else you want to say to Aiko Chan?")
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


def initialize_new_game_not_understood():
    return Game(NotUnderstood(), Session(SessionState(None)))


def initialize_new_stop_game(session):
    return Game(SessionEndedRequest(), session)


def initialize_new_help_game(session):
    return Game(HelpIntent(), session)


def get_questions_you_can_ask():
    random_int = random.randint(1, 17)
    if random_int == 1:
        return "\"What are you doing\""
    elif random_int == 2:
        return "\"What are you thinking\""
    elif random_int == 3:
        return "\"how are you feeling\""
    elif random_int == 4:
        return "\"Alexa, tell aiko chan that I am home\""
    elif random_int == 5:
        return "\"I'm heading out\""
    elif random_int == 6:
        return "\"Good morning\""
    elif random_int == 7:
        return "\"Good night\""
    elif random_int == 8:
        return "\"I love you\""
    elif random_int == 9:
        return "\"Did you miss me\""
    elif random_int == 10:
        return "\"Do you love me\""
    elif random_int == 11:
        return "\"Switch to tsundere mode\""
    elif random_int == 12:
        return "\"Switch to normal mode\""
    elif random_int == 13:
        return "\"What can I buy\""
    elif random_int == 14:
        return "\"Tell me more about tsudere mode\""
    elif random_int == 15:
        return "\"Tell me more about the date\""
    elif random_int == 16:
        return "\"Who are you\""
    elif random_int == 17:
        return "\"Let's go on a date\""
