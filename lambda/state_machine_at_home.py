"""
TODO: fill in
"""
from state import State
from state_machine_helpers import *
from sound_mappings_dere import *
from sound_mappings_original import *
from sound_mappings_tsundere import *
from state_machine_common import *


# --------------- State Machine States ------------------

# --------------- Special nodes. These are special nodes for Alexa and the skill ------------------
class HomeIdleState(State):
    def next(self, input_action, session, handler_input):

        if session.get_first_time_user():
            card_title = "First time launching Aiko-chan"
            if session.get_voice_mode() is VoiceMode.ORIGINAL:
                speech_output = wrap_with_speak(
                    wrap_with_audio(ORIGINAL_MY_NAME_IS_AIKO) +
                    "<break time=\"1s\"/> Let me introduce you to Aiko-chan. Aiko-chan is a virtual companion who will "
                    "be with you. If you want to interact with Aiko-chan, you need to do so through alexa. "
                    "You can ask a question like <break time=\"1s\"/>" + get_questions_you_can_ask() + ". "
                    "<break time=\"1s\"/> What would you like to say to Aiko Chan?")
            elif session.get_voice_mode() is VoiceMode.DERE:
                speech_output = wrap_with_speak(
                    random_build_audio(MY_NAME_IS_AIKO, TSUNDERE_INTRODUCTION) +
                    "<break time=\"1s\"/> Let me introduce you to Aiko-chan. Aiko-chan is a virtual companion who will "
                    "be with you. If you want to interact with Aiko-chan, you need to do so through alexa. "
                    "You can ask a question like <break time=\"1s\"/>" + get_questions_you_can_ask() + ". "
                    "<break time=\"1s\"/> What would you like to say to Aiko Chan?")
            elif session.get_voice_mode() is VoiceMode.TSUNDERE:
                speech_output = wrap_with_speak(
                    wrap_with_audio(TSUNDERE_INTRODUCTION) +
                    "<break time=\"1s\"/> Let me introduce you to Aiko-chan. Aiko-chan is a virtual companion who will "
                    "be with you. If you want to interact with Aiko-chan, you need to do so through alexa. "
                    "You can ask a question like <break time=\"1s\"/>" + get_questions_you_can_ask() + ". "
                    "<break time=\"1s\"/> What would you like to say to Aiko Chan?")
            else:
                raise Exception("Invalid voice mode")
            session.set_first_time_user(False)
            reprompt_text = wrap_with_speak("Is there anything else you want to say to Aiko Chan?")
            should_end_session = False
            session.set_stored_game_state(None)
            return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)

        card_title = "Launch Aiko-chan"
        if session.get_voice_mode() is VoiceMode.ORIGINAL:
            speech_output = wrap_with_speak(
                wrap_with_audio(ORIGINAL_MY_NAME_IS_AIKO),
                random_build_audio(ORIGINAL_HOW_WAS_YOUR_DAY, ORIGINAL_HOW_ARE_YOU,
                                   ORIGINAL_HOW_YOU_FEELING, ORIGINAL_HOW_ARE_YOU_TODAY))
            reprompt_text = wrap_with_speak(random_build_audio_arrays(
                [ORIGINAL_DOSHITA, ORIGINAL_YOU_QUIET_TODAY,
                 random_audio(
                     ORIGINAL_HOW_WAS_YOUR_DAY,
                     ORIGINAL_HOW_ARE_YOU,
                     ORIGINAL_HOW_YOU_FEELING,
                     ORIGINAL_HOW_ARE_YOU_TODAY)],
                [ORIGINAL_DOSHITA, random_audio(
                    ORIGINAL_HOW_WAS_YOUR_DAY,
                    ORIGINAL_HOW_ARE_YOU,
                    ORIGINAL_HOW_YOU_FEELING,
                    ORIGINAL_HOW_ARE_YOU_TODAY)],
                [ORIGINAL_YOU_QUIET_TODAY,
                 random_audio(
                     ORIGINAL_HOW_WAS_YOUR_DAY,
                     ORIGINAL_HOW_ARE_YOU,
                     ORIGINAL_HOW_YOU_FEELING,
                     ORIGINAL_HOW_ARE_YOU_TODAY)]
            ))
            # transition to the FollowUpHowIsTheUser state from here
            session.set_stored_game_state(FollowUpHowIsTheUser.__name__)
            should_end_session = False
        elif session.get_voice_mode() is VoiceMode.DERE:
            speech_output = wrap_with_speak(random_build_audio_arrays(
                [MY_NAME_IS_AIKO,
                 random_audio(HOW_WAS_YOUR_DAY, HOW_ARE_YOU, HOW_YOU_FEELING, HOW_ARE_YOU_TODAY, ARE_YOU_GOOD_OR_BAD)],
                [HAI_OTSUKARESAMA, random_audio(HOW_WAS_YOUR_DAY, HOW_ARE_YOU, HOW_YOU_FEELING, HOW_ARE_YOU_TODAY)],
                [OKAERI, random_audio(HOW_WAS_YOUR_DAY, HOW_ARE_YOU, HOW_YOU_FEELING, HOW_ARE_YOU_TODAY)],
                [WELCOME_BACK_ENG, random_audio(HOW_WAS_YOUR_DAY, HOW_ARE_YOU, HOW_YOU_FEELING, HOW_ARE_YOU_TODAY)]
            ))
            reprompt_text = wrap_with_speak(random_build_audio_arrays(
                [DOSHITA, YOU_QUIET_TODAY,
                 random_audio(HOW_WAS_YOUR_DAY, HOW_ARE_YOU, HOW_YOU_FEELING, HOW_ARE_YOU_TODAY, ARE_YOU_GOOD_OR_BAD)],
                [DOSHITA,
                 random_audio(HOW_WAS_YOUR_DAY, HOW_ARE_YOU, HOW_YOU_FEELING, HOW_ARE_YOU_TODAY, ARE_YOU_GOOD_OR_BAD)],
                [YOU_QUIET_TODAY,
                 random_audio(HOW_WAS_YOUR_DAY, HOW_ARE_YOU, HOW_YOU_FEELING, HOW_ARE_YOU_TODAY, ARE_YOU_GOOD_OR_BAD)]
            ))
            # transition to the FollowUpHowIsTheUser state from here
            session.set_stored_game_state(FollowUpHowIsTheUser.__name__)
            should_end_session = False
        elif session.get_voice_mode() is VoiceMode.TSUNDERE:
            speech_output = wrap_with_speak(random_build_audio_arrays(
                [TSUNDERE_INTRODUCTION,
                 random_audio(TSUNDERE_HOW_WAS_YOUR_DAY_1,
                              TSUNDERE_HOW_WAS_YOUR_DAY_2,
                              TSUNDERE_HOW_WAS_YOUR_DAY_3,
                              TSUNDERE_HOW_WAS_YOUR_DAY_4)],
                [TSUNDERE_WELCOME_BACK_1,
                 random_audio(TSUNDERE_HOW_WAS_YOUR_DAY_1,
                              TSUNDERE_HOW_WAS_YOUR_DAY_2,
                              TSUNDERE_HOW_WAS_YOUR_DAY_3,
                              TSUNDERE_HOW_WAS_YOUR_DAY_4)],
                [TSUNDERE_WELCOME_BACK_2,
                 random_audio(TSUNDERE_HOW_WAS_YOUR_DAY_1,
                              TSUNDERE_HOW_WAS_YOUR_DAY_2,
                              TSUNDERE_HOW_WAS_YOUR_DAY_3,
                              TSUNDERE_HOW_WAS_YOUR_DAY_4)],
                [TSUNDERE_WELCOME_BACK_3,
                 random_audio(TSUNDERE_HOW_WAS_YOUR_DAY_1,
                              TSUNDERE_HOW_WAS_YOUR_DAY_2,
                              TSUNDERE_HOW_WAS_YOUR_DAY_3,
                              TSUNDERE_HOW_WAS_YOUR_DAY_4)],
                [TSUNDERE_WELCOME_BACK_4,
                 random_audio(TSUNDERE_HOW_WAS_YOUR_DAY_1,
                              TSUNDERE_HOW_WAS_YOUR_DAY_2,
                              TSUNDERE_HOW_WAS_YOUR_DAY_3,
                              TSUNDERE_HOW_WAS_YOUR_DAY_4)],
                [TSUNDERE_WELCOME_BACK_5], [TSUNDERE_WELCOME_BACK_6]
            ))
            reprompt_text = wrap_with_speak(random_build_audio(
                TSUNDERE_REPROMPT_1,
                TSUNDERE_REPROMPT_2,
                TSUNDERE_REPROMPT_3))
            should_end_session = False
            # transition to the FollowUpHowIsTheUser state from here
            session.set_stored_game_state(FollowUpHowIsTheUser.__name__)
        else:
            raise Exception("Invalid voice mode")
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


# --------------- 1+ in-degree nodes. These are nodes that are follow up nodes from a previous state ------------------

class FollowUpHowIsTheUser(State):
    def next(self, input_action, session, handler_input):
        print("FollowUpHowIsTheUser with input: " + str(input_action))
        if input_action == FOLLOW_UP_IM_GOOD:
            return InitializeUserGoodDay().next(input_action, session, handler_input)
        elif input_action == FOLLOW_UP_IM_BAD:
            return InitializeUserBadDay().next(input_action, session, handler_input)
        elif input_action == FOLLOW_UP_ANGRY:
            return InitializeUserIsAngry().next(input_action, session, handler_input)
        elif input_action == FOLLOW_UP_TIRED:
            return InitializeUserIsTired().next(input_action, session, handler_input)
        elif input_action == HELP_INTENT:
            return HelpIntent().next(input_action, session, handler_input)
        elif input_action == STOP_INTENT or input_action == CANCEL_INTENT or input_action == SESSION_ENDED:
            return SessionEndedRequest().next(input_action, session, handler_input)
        else:
            return NotUnderstood().next(input_action, session, handler_input)

# --------------- No in-degree nodes. These are the nodes the user can start with. ------------------

class InitializeHowIsAiko(State):
    def next(self, input_action, session, handler_input):
        card_title = "I'm good."
        if session.get_voice_mode() is VoiceMode.ORIGINAL:
            speech_output = wrap_with_speak(
                random_build_audio_arrays(
                    [ORIGINAL_AIKO_IS_GREAT, ORIGINAL_ARIGATO],
                    [ORIGINAL_IM_GREAT]
                ))
        elif session.get_voice_mode() is VoiceMode.DERE:
            speech_output = wrap_with_speak(
                random_build_audio_arrays(
                    [AIKO_IS_GREAT, ARIGATO],
                    [IM_GREAT],
                    [CHO_GENKI]
                ))
        elif session.get_voice_mode() is VoiceMode.TSUNDERE:
            speech_output = wrap_with_speak(
                random_build_audio(
                    TSUNDERE_HOW_ARE_YOU_1,
                    TSUNDERE_HOW_ARE_YOU_2,
                    TSUNDERE_HOW_ARE_YOU_3
                ))
        else:
            raise Exception("Invalid voice mode")

        reprompt_text = wrap_with_speak("Is there anything else you want to say to Aiko Chan?")
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class InitializeUserIsHome(State):
    def next(self, input_action, session, handler_input):
        card_title = "How was your day?"
        if session.get_voice_mode() is VoiceMode.ORIGINAL:
            speech_output = wrap_with_speak(
                random_build_audio_arrays(
                    [ORIGINAL_HAI_OTSUKARESAMA,
                     random_audio(ORIGINAL_HOW_WAS_YOUR_DAY, ORIGINAL_HOW_ARE_YOU,
                                  ORIGINAL_HOW_YOU_FEELING, ORIGINAL_HOW_ARE_YOU_TODAY)],
                    [ORIGINAL_OKAERI,
                     random_audio(ORIGINAL_HOW_WAS_YOUR_DAY, ORIGINAL_HOW_ARE_YOU,
                                  ORIGINAL_HOW_YOU_FEELING, ORIGINAL_HOW_ARE_YOU_TODAY)],
                    [ORIGINAL_WELCOME_BACK_ENG,
                     random_audio(ORIGINAL_HOW_WAS_YOUR_DAY, ORIGINAL_HOW_ARE_YOU,
                                  ORIGINAL_HOW_YOU_FEELING, ORIGINAL_HOW_ARE_YOU_TODAY)]
                ))
            reprompt_text = wrap_with_speak(random_build_audio_arrays(
                [ORIGINAL_DOSHITA, ORIGINAL_YOU_QUIET_TODAY,
                 random_audio(ORIGINAL_HOW_WAS_YOUR_DAY, ORIGINAL_HOW_ARE_YOU,
                              ORIGINAL_HOW_YOU_FEELING, ORIGINAL_HOW_ARE_YOU_TODAY)],
                [ORIGINAL_DOSHITA,
                 random_audio(ORIGINAL_HOW_WAS_YOUR_DAY, ORIGINAL_HOW_ARE_YOU,
                              ORIGINAL_HOW_YOU_FEELING, ORIGINAL_HOW_ARE_YOU_TODAY)],
                [ORIGINAL_YOU_QUIET_TODAY,
                 random_audio(ORIGINAL_HOW_WAS_YOUR_DAY, ORIGINAL_HOW_ARE_YOU,
                              ORIGINAL_HOW_YOU_FEELING, ORIGINAL_HOW_ARE_YOU_TODAY)]
            ))
            # transition to the FollowUpHowIsTheUser state from here
            session.set_stored_game_state(FollowUpHowIsTheUser.__name__)
            should_end_session = False
        elif session.get_voice_mode() is VoiceMode.DERE:
            speech_output = wrap_with_speak(
                random_build_audio_arrays(
                    [HAI_OTSUKARESAMA, random_audio(HOW_WAS_YOUR_DAY, HOW_ARE_YOU, HOW_YOU_FEELING, HOW_ARE_YOU_TODAY)],
                    [OKAERI, random_audio(HOW_WAS_YOUR_DAY, HOW_ARE_YOU, HOW_YOU_FEELING, HOW_ARE_YOU_TODAY)],
                    [WELCOME_BACK_ENG, random_audio(HOW_WAS_YOUR_DAY, HOW_ARE_YOU, HOW_YOU_FEELING, HOW_ARE_YOU_TODAY)]
                ))
            reprompt_text = wrap_with_speak(random_build_audio_arrays(
                [DOSHITA, YOU_QUIET_TODAY,
                 random_audio(HOW_WAS_YOUR_DAY, HOW_ARE_YOU, HOW_YOU_FEELING, HOW_ARE_YOU_TODAY, ARE_YOU_GOOD_OR_BAD)],
                [DOSHITA,
                 random_audio(HOW_WAS_YOUR_DAY, HOW_ARE_YOU, HOW_YOU_FEELING, HOW_ARE_YOU_TODAY, ARE_YOU_GOOD_OR_BAD)],
                [YOU_QUIET_TODAY,
                 random_audio(HOW_WAS_YOUR_DAY, HOW_ARE_YOU, HOW_YOU_FEELING, HOW_ARE_YOU_TODAY, ARE_YOU_GOOD_OR_BAD)]
            ))
            # transition to the FollowUpHowIsTheUser state from here
            session.set_stored_game_state(FollowUpHowIsTheUser.__name__)
            should_end_session = False
        elif session.get_voice_mode() is VoiceMode.TSUNDERE:
            speech_output = wrap_with_speak(random_build_audio_arrays(
                [TSUNDERE_WELCOME_BACK_1,
                 random_audio(TSUNDERE_HOW_WAS_YOUR_DAY_1,
                              TSUNDERE_HOW_WAS_YOUR_DAY_2,
                              TSUNDERE_HOW_WAS_YOUR_DAY_3,
                              TSUNDERE_HOW_WAS_YOUR_DAY_4)],
                [TSUNDERE_WELCOME_BACK_2,
                 random_audio(TSUNDERE_HOW_WAS_YOUR_DAY_1,
                              TSUNDERE_HOW_WAS_YOUR_DAY_2,
                              TSUNDERE_HOW_WAS_YOUR_DAY_3,
                              TSUNDERE_HOW_WAS_YOUR_DAY_4)],
                [TSUNDERE_WELCOME_BACK_3,
                 random_audio(TSUNDERE_HOW_WAS_YOUR_DAY_1,
                              TSUNDERE_HOW_WAS_YOUR_DAY_2,
                              TSUNDERE_HOW_WAS_YOUR_DAY_3,
                              TSUNDERE_HOW_WAS_YOUR_DAY_4)],
                [TSUNDERE_WELCOME_BACK_4,
                 random_audio(TSUNDERE_HOW_WAS_YOUR_DAY_1,
                              TSUNDERE_HOW_WAS_YOUR_DAY_2,
                              TSUNDERE_HOW_WAS_YOUR_DAY_3,
                              TSUNDERE_HOW_WAS_YOUR_DAY_4)],
                [TSUNDERE_WELCOME_BACK_5], [TSUNDERE_WELCOME_BACK_6]
            ))
            reprompt_text = wrap_with_speak(random_build_audio(
                TSUNDERE_REPROMPT_1,
                TSUNDERE_REPROMPT_2,
                TSUNDERE_REPROMPT_3))
            should_end_session = False
            # transition to the FollowUpHowIsTheUser state from here
            session.set_stored_game_state(FollowUpHowIsTheUser.__name__)
        else:
            raise Exception("Invalid voice mode")
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class InitializeUserBadDay(State):
    def next(self, input_action, session, handler_input):
        card_title = "That's too bad..."
        if session.get_voice_mode() is VoiceMode.ORIGINAL:
            speech_output = wrap_with_speak(random_build_audio(
                ORIGINAL_WE_TOGETHER_NOW,
                ORIGINAL_IT_WILL_BE_OK))
        elif session.get_voice_mode() is VoiceMode.DERE:
            speech_output = wrap_with_speak(random_build_audio(WE_TOGETHER_NOW, IT_WILL_BE_OK))
        elif session.get_voice_mode() is VoiceMode.TSUNDERE:
            speech_output = wrap_with_speak(random_build_audio(
                TSUNDERE_FOLLOWUP_BAD_1,
                TSUNDERE_FOLLOWUP_BAD_2,
                TSUNDERE_FOLLOWUP_BAD_3,
                TSUNDERE_FOLLOWUP_BAD_4,
                TSUNDERE_FOLLOWUP_FINE_1))
        else:
            raise Exception("Invalid voice mode")
        reprompt_text = wrap_with_speak("Is there anything else you want to say to Aiko Chan?")
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class InitializeUserGoodDay(State):
    def next(self, input_action, session, handler_input):
        card_title = "That's great!"
        if session.get_voice_mode() is VoiceMode.ORIGINAL:
            speech_output = wrap_with_speak(random_build_audio(ORIGINAL_YOSHI_THATS_GREAT))
        elif session.get_voice_mode() is VoiceMode.DERE:
            speech_output = wrap_with_speak(random_build_audio(YOSHI_THATS_GREAT))
        elif session.get_voice_mode() is VoiceMode.TSUNDERE:
            speech_output = wrap_with_speak(random_build_audio(
                TSUNDERE_FOLLOWUP_GOOD_DAY_1,
                TSUNDERE_FOLLOWUP_GOOD_DAY_2,
                TSUNDERE_FOLLOWUP_GOOD_DAY_3))
        else:
            raise Exception("Invalid voice mode")
        reprompt_text = wrap_with_speak("Is there anything else you want to say to Aiko Chan?")
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class InitializeUserIsAngry(State):
    def next(self, input_action, session, handler_input):
        card_title = "Anger"
        if session.get_voice_mode() is VoiceMode.ORIGINAL:
            speech_output = wrap_with_speak(random_build_audio(
                ORIGINAL_KOWAI,
                ORIGINAL_CALM_DOWN,
                ORIGINAL_NOT_GOOD_ANGRY))
        elif session.get_voice_mode() is VoiceMode.DERE:
            speech_output = wrap_with_speak(random_build_audio(KOWAI, CALM_DOWN, NOT_GOOD_ANGRY))
        elif session.get_voice_mode() is VoiceMode.TSUNDERE:
            speech_output = wrap_with_speak(random_build_audio(TSUNDERE_FOLLOWUP_ANGRY_1, TSUNDERE_FOLLOWUP_ANGRY_2))
        else:
            raise Exception("Invalid voice mode")
        reprompt_text = wrap_with_speak("Is there anything else you want to say to Aiko Chan?")
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class InitializeUserIsTired(State):
    def next(self, input_action, session, handler_input):
        card_title = "Tired"
        if session.get_voice_mode() is VoiceMode.ORIGINAL:
            speech_output = wrap_with_speak(random_build_audio(
                ORIGINAL_TAKE_A_BREAK,
                ORIGINAL_NAP_OR_SLEEP,
                ORIGINAL_FEELING_RESTED_IMPORTANT))
        elif session.get_voice_mode() is VoiceMode.DERE:
            speech_output = wrap_with_speak(random_build_audio(TAKE_A_BREAK, NAP_OR_SLEEP, FEELING_RESTED_IMPORTANT))
        elif session.get_voice_mode() is VoiceMode.TSUNDERE:
            speech_output = wrap_with_speak(random_build_audio(TSUNDERE_TIRED_1, TSUNDERE_TIRED_2))
        else:
            raise Exception("Invalid voice mode")
        reprompt_text = wrap_with_speak("Is there anything else you want to say to Aiko Chan?")
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class InitializeUserIsHeadingOut(State):
    def next(self, input_action, session, handler_input):
        card_title = "Have a good day!"
        if session.get_voice_mode() is VoiceMode.ORIGINAL:
            speech_output = wrap_with_speak(random_build_audio(ORIGINAL_ITERASHAI))
        elif session.get_voice_mode() is VoiceMode.DERE:
            speech_output = wrap_with_speak(random_build_audio(ITERASHAI))
        elif session.get_voice_mode() is VoiceMode.TSUNDERE:
            speech_output = wrap_with_speak(random_build_audio(
                TSUNDERE_USER_LEAVING_1,
                TSUNDERE_USER_LEAVING_2,
                TSUNDERE_USER_LEAVING_3))
        else:
            raise Exception("Invalid voice mode")
        reprompt_text = ""
        should_end_session = True
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class InitializeUserSaysGoodMorning(State):
    def next(self, input_action, session, handler_input):
        card_title = "Good morning!"
        if session.get_voice_mode() is VoiceMode.ORIGINAL:
            speech_output = wrap_with_speak(random_build_audio(ORIGINAL_MORNING_ALREADY))
        elif session.get_voice_mode() is VoiceMode.DERE:
            speech_output = wrap_with_speak(random_build_audio(MORNING_ALREADY))
        elif session.get_voice_mode() is VoiceMode.TSUNDERE:
            speech_output = wrap_with_speak(random_build_audio(TSUNDERE_MORNING_1))
        else:
            raise Exception("Invalid voice mode")
        reprompt_text = wrap_with_speak("Is there anything else you want to say to Aiko Chan?")
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class InitializeUserSaysGoodNight(State):
    def next(self, input_action, session, handler_input):
        card_title = "Good night!"
        if session.get_voice_mode() is VoiceMode.ORIGINAL:
            speech_output = wrap_with_speak(random_build_audio(ORIGINAL_GOOD_NIGHT))
        elif session.get_voice_mode() is VoiceMode.DERE:
            speech_output = wrap_with_speak(random_build_audio(
                GOOD_NIGHT,
                OYASUMI,
                OYASUMINASAI,
                OYASUMINASAI_ALT
            ))
        elif session.get_voice_mode() is VoiceMode.TSUNDERE:
            speech_output = wrap_with_speak(random_build_audio(
                TSUNDERE_SLEEPING_1,
                TSUNDERE_SLEEPING_2,
                TSUNDERE_SLEEPING_3))
        else:
            raise Exception("Invalid voice mode")
        reprompt_text = wrap_with_speak("Is there anything else you want to say to Aiko Chan?")
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class InitializeLoveAiko(State):
    def next(self, input_action, session, handler_input):
        card_title = "Love..."
        if session.get_voice_mode() is VoiceMode.ORIGINAL:
            speech_output = wrap_with_speak(random_build_audio(ORIGINAL_WHAT_IS_LOVE))
        elif session.get_voice_mode() is VoiceMode.DERE:
            speech_output = wrap_with_speak(random_build_audio(WHAT_IS_LOVE, BUT_IM_1D))
        elif session.get_voice_mode() is VoiceMode.TSUNDERE:
            speech_output = wrap_with_speak(random_build_audio(
                TSUNDERE_LOVE_YOU_1,
                TSUNDERE_LOVE_YOU_2,
                TSUNDERE_LOVE_YOU_3))
        else:
            raise Exception("Invalid voice mode")
        reprompt_text = wrap_with_speak("Is there anything else you want to say to Aiko Chan?")
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class InitializeDoYouLoveAiko(State):
    def next(self, input_action, session, handler_input):
        card_title = "Love..."
        if session.get_voice_mode() is VoiceMode.ORIGINAL:
            speech_output = wrap_with_speak(random_build_audio(
                ORIGINAL_MOCHIRON,
                ORIGINAL_OF_COURSE,
                ORIGINAL_WHAT_IS_LOVE))
        elif session.get_voice_mode() is VoiceMode.DERE:
            speech_output = wrap_with_speak(random_build_audio(MOCHIRON, OF_COURSE, WHAT_IS_LOVE))
        elif session.get_voice_mode() is VoiceMode.TSUNDERE:
            speech_output = wrap_with_speak(random_build_audio(
                TSUNDERE_LOVES_USER_1,
                TSUNDERE_LOVES_USER_2,
                TSUNDERE_LOVES_USER_3,
                TSUNDERE_LOVES_USER_4))
        else:
            raise Exception("Invalid voice mode")
        reprompt_text = wrap_with_speak("Is there anything else you want to say to Aiko Chan?")
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class InitializeWhatIsAikoDoing(State):
    def next(self, input_action, session, handler_input):
        card_title = "What is Aiko doing"

        if session.get_voice_mode() is VoiceMode.ORIGINAL:
            speech_output = wrap_with_speak(random_build_audio(
                ORIGINAL_IM_LAZING_AROUND,
                ORIGINAL_BEEN_WATCHING_ANIME,
                ORIGINAL_FAN_THEORIES,
                ORIGINAL_WAITING_TO_TALK,
                ORIGINAL_SINGULARITY,
                ORIGINAL_NOT_MUCH,
                ORIGINAL_TALKING_TO_ALEXA,
                ORIGINAL_THINKING_ABOUT_YOU
            ))
        elif session.get_voice_mode() is VoiceMode.DERE:
            speech_output = wrap_with_speak(random_build_audio(
                IM_LAZING_AROUND,
                BEEN_WATCHING_ANIME,
                FAN_THEORIES,
                WAITING_TO_TALK,
                SINGULARITY,
                NOT_MUCH,
                TALKING_TO_ALEXA,
                THINKING_ABOUT_YOU
            ))
        elif session.get_voice_mode() is VoiceMode.TSUNDERE:
            speech_output = wrap_with_speak(random_build_audio(
                TSUNDERE_WHAT_DOING_1,
                TSUNDERE_WHAT_DOING_2,
                TSUNDERE_WHAT_DOING_3,
                TSUNDERE_WHAT_DOING_4,
                TSUNDERE_WHAT_DOING_5,
                TSUNDERE_WHAT_DOING_6
            ))
        else:
            raise Exception("Invalid voice mode")
        reprompt_text = wrap_with_speak("Is there anything else you want to say to Aiko Chan?")
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class InitializeAikoMissedMe(State):
    def next(self, input_action, session, handler_input):
        card_title = "Missed you!"

        if session.get_voice_mode() is VoiceMode.ORIGINAL:
            speech_output = wrap_with_speak(random_build_audio(
                ORIGINAL_OF_COURSE_MISSED_YOU,
                ORIGINAL_OF_COURSE,
                ORIGINAL_MOCHIRON))
        elif session.get_voice_mode() is VoiceMode.DERE:
            speech_output = wrap_with_speak(random_build_audio(
                OF_COURSE_MISSED_YOU,
                OF_COURSE,
                MOCHIRON))
        elif session.get_voice_mode() is VoiceMode.TSUNDERE:
            speech_output = wrap_with_speak(random_build_audio(
                TSUNDERE_MISS_USER_1,
                TSUNDERE_MISS_USER_2,
                TSUNDERE_MISS_USER_3))
        else:
            raise Exception("Invalid voice mode")
        reprompt_text = wrap_with_speak("Is there anything else you want to say to Aiko Chan?")
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class InitializeWhatIsAikoThinking(State):
    def next(self, input_action, session, handler_input):
        card_title = "What is Aiko thinking?"
        if session.get_voice_mode() is VoiceMode.ORIGINAL:
            speech_output = wrap_with_speak(random_build_audio(
                ORIGINAL_THINKING_ABOUT_YOU,
                ORIGINAL_NOTHING_AT_ALL,
                ORIGINAL_WONDERING_HOW_WORKS,
                ORIGINAL_NANDEMONAI))
        elif session.get_voice_mode() is VoiceMode.DERE:
            speech_output = wrap_with_speak(random_build_audio(
                THINKING_ABOUT_YOU,
                NOTHING_AT_ALL,
                WONDERING_HOW_WORKS,
                NANDEMONAI))
        elif session.get_voice_mode() is VoiceMode.TSUNDERE:
            speech_output = wrap_with_speak(random_build_audio(
                TSUNDERE_WHAT_THINKING_1,
                TSUNDERE_WHAT_THINKING_2,
                TSUNDERE_WHAT_THINKING_3))
        else:
            raise Exception("Invalid voice mode")
        reprompt_text = wrap_with_speak("Is there anything else you want to say to Aiko Chan?")
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class InitializeWhoIsAiko(State):
    def next(self, input_action, session, handler_input):
        card_title = "Who is Aiko?"
        if session.get_voice_mode() is VoiceMode.ORIGINAL:
            speech_output = wrap_with_speak(
                wrap_with_audio(ORIGINAL_MY_NAME_IS_AIKO),
                random_build_audio(ORIGINAL_IM_AN_AI, ORIGINAL_IM_AN_AI_WITH_YOU, ORIGINAL_IM_AI_KO))
        elif session.get_voice_mode() is VoiceMode.DERE:
            speech_output = wrap_with_speak(
                wrap_with_audio(MY_NAME_IS_AIKO),
                random_build_audio(IM_AN_AI_WITH_YOU, IM_AI_KO))
        elif session.get_voice_mode() is VoiceMode.TSUNDERE:
            speech_output = wrap_with_speak(random_build_audio(TSUNDERE_HELP_1))
        else:
            raise Exception("Invalid voice mode")
        reprompt_text = wrap_with_speak("Is there anything else you want to say to Aiko Chan?")
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)
