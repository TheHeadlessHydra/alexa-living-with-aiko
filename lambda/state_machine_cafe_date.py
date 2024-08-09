from state import State
from state_machine_helpers import *
from sound_mappings_cafe_date import *
from sound_mappings_tsundere import *
from state_machine_common import *
from in_skill_purchase import CAFE_DATE_PRODUCT_ID


class CommandInitiateDate(State):
    def next(self, input_action, session, handler_input):
        card_title = "Go on a date?"

        if not session.get_is_cafe_date_purchased() and session.get_is_cafe_date_purchasable():
            speech_output = wrap_with_speak("")
            should_end_session = True
            reprompt_text = ""
            return_object = get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)
            return add_upsell_to_output(return_object, CAFE_DATE_PRODUCT_ID,
                                        "The cafe date is not available right now. Would you like to hear more?")
        elif not session.get_is_cafe_date_purchased() and not session.get_is_cafe_date_purchasable():
            speech_output = wrap_with_speak("We are sorry, but the cafe date is not enabled or purchasable in your region. "
                                            "Is there anything else you want to say to Aiko Chan?")
            should_end_session = False
            reprompt_text = wrap_with_speak("Is there anything else you want to say to Aiko Chan?")
        else:
            speech_output = wrap_with_speak(
                random_build_audio(CAFE_DATE_INITIALIZE_1, CAFE_DATE_INITIALIZE_2, CAFE_DATE_INITIALIZE_3, CAFE_DATE_INITIALIZE_4),
                wrap_with_audio(CAFE_DATE_INTRO_DOOR_SOUNDS),
                random_build_audio(CAFE_DATE_OPENING_1, CAFE_DATE_OPENING_2),
                random_build_audio(CAFE_DATE_OPENING_Q_1, CAFE_DATE_OPENING_Q_2)
            )
            should_end_session = False
            session.set_is_in_cafe_date(True)
            reprompt_text = wrap_with_speak(
                random_build_audio(CAFE_DATE_REPROMPT_1, CAFE_DATE_REPROMPT_2, CAFE_DATE_REPROMPT_3, CAFE_DATE_REPROMPT_4)
            )

        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class NotUnderstoodCafeDate(State):
    def next(self, input_action, session, handler_input):
        card_title = "Did not understand"
        # TODO add "date like question" to the end of this
        speech_output = wrap_with_speak(
            random_build_audio(
                TSUNDERE_DIDNT_UNDERSTAND_1,
                TSUNDERE_DIDNT_UNDERSTAND_2,
                TSUNDERE_DIDNT_UNDERSTAND_3
            ),
            wrap_with_audio(CAFE_DATE_ASK_ME_DATE_LIKE_QUESTION)
        )
        reprompt_text = wrap_with_speak(
            random_build_audio(CAFE_DATE_REPROMPT_1, CAFE_DATE_REPROMPT_2, CAFE_DATE_REPROMPT_3, CAFE_DATE_REPROMPT_4)
        )
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class CafeDateGoHome(State):
    def next(self, input_action, session, handler_input):
        card_title = "End the date"
        speech_output = wrap_with_speak(
            random_build_audio(
                CAFE_DATE_LEAVING_1,
                CAFE_DATE_LEAVING_2,
                CAFE_DATE_LEAVING_3
            )
        )
        reprompt_text = wrap_with_speak("Is there anything else you want to say to Aiko Chan?")
        should_end_session = False
        session.set_is_in_cafe_date(False)
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class CafeDateWhatToOrder(State):
    def next(self, input_action, session, handler_input):
        card_title = "What to order?"
        speech_output = wrap_with_speak(
            random_build_audio(
                CAFE_DATE_WHAT_TO_ORDER_1,
                CAFE_DATE_WHAT_TO_ORDER_2,
                CAFE_DATE_WHAT_TO_ORDER_3
            )
        )
        reprompt_text = wrap_with_speak(
            random_build_audio(CAFE_DATE_REPROMPT_1, CAFE_DATE_REPROMPT_2, CAFE_DATE_REPROMPT_3, CAFE_DATE_REPROMPT_4)
        )
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class CafeDateHowWasDay(State):
    def next(self, input_action, session, handler_input):
        card_title = "What to order?"
        speech_output = wrap_with_speak(
            random_build_audio(
                CAFE_DATE_HOW_WAS_YOUR_DAY_1,
                CAFE_DATE_HOW_WAS_YOUR_DAY_2
            )
        )
        reprompt_text = wrap_with_speak(
            random_build_audio(CAFE_DATE_REPROMPT_1, CAFE_DATE_REPROMPT_2, CAFE_DATE_REPROMPT_3, CAFE_DATE_REPROMPT_4)
        )
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class CafeDateWhatAboutThisPlace(State):
    def next(self, input_action, session, handler_input):
        card_title = "What to order?"
        speech_output = wrap_with_speak(
            random_build_audio(
                CAFE_DATE_WHAT_ABOUT_PLACE_1,
                CAFE_DATE_WHAT_ABOUT_PLACE_2
            )
        )
        reprompt_text = wrap_with_speak(
            random_build_audio(CAFE_DATE_REPROMPT_1, CAFE_DATE_REPROMPT_2, CAFE_DATE_REPROMPT_3, CAFE_DATE_REPROMPT_4)
        )
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class CafeDateFoodLike(State):
    def next(self, input_action, session, handler_input):
        card_title = "What to order?"
        speech_output = wrap_with_speak(
            random_build_audio(
                CAFE_DATE_WHAT_FOOD_YOU_LIKE_1,
                CAFE_DATE_WHAT_FOOD_YOU_LIKE_2,
                CAFE_DATE_WHAT_FOOD_YOU_LIKE_3
            )
        )
        reprompt_text = wrap_with_speak(
            random_build_audio(CAFE_DATE_REPROMPT_1, CAFE_DATE_REPROMPT_2, CAFE_DATE_REPROMPT_3,
                               CAFE_DATE_REPROMPT_4)
        )
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class CafeDateWhatTypeOfPartner(State):
    def next(self, input_action, session, handler_input):
        card_title = "What to order?"
        speech_output = wrap_with_speak(
            random_build_audio(
                CAFE_DATE_WHAT_LOOK_FOR_IN_PARTNER_1,
                CAFE_DATE_WHAT_LOOK_FOR_IN_PARTNER_2
            )
        )
        reprompt_text = wrap_with_speak(
            random_build_audio(CAFE_DATE_REPROMPT_1, CAFE_DATE_REPROMPT_2, CAFE_DATE_REPROMPT_3,
                               CAFE_DATE_REPROMPT_4)
        )
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class CafeDateEverBeenInLove(State):
    def next(self, input_action, session, handler_input):
        card_title = "What to order?"
        speech_output = wrap_with_speak(
            random_build_audio(
                CAFE_DATE_EVER_BEEN_IN_LOVE_1,
                CAFE_DATE_EVER_BEEN_IN_LOVE_2,
                CAFE_DATE_EVER_BEEN_IN_LOVE_3,
                CAFE_DATE_EVER_BEEN_IN_LOVE_4
            )
        )
        reprompt_text = wrap_with_speak(
            random_build_audio(CAFE_DATE_REPROMPT_1, CAFE_DATE_REPROMPT_2, CAFE_DATE_REPROMPT_3,
                               CAFE_DATE_REPROMPT_4)
        )
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class CafeDateWantKids(State):
    def next(self, input_action, session, handler_input):
        card_title = "What to order?"
        speech_output = wrap_with_speak(
            random_build_audio(
                CAFE_DATE_WANT_KIDS_1
            )
        )
        reprompt_text = wrap_with_speak(
            random_build_audio(CAFE_DATE_REPROMPT_1, CAFE_DATE_REPROMPT_2, CAFE_DATE_REPROMPT_3,
                               CAFE_DATE_REPROMPT_4)
        )
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class CafeDateWhatMakesLaugh(State):
    def next(self, input_action, session, handler_input):
        card_title = "What to order?"
        speech_output = wrap_with_speak(
            random_build_audio(
                CAFE_DATE_WHAT_LAUGH_1,
                CAFE_DATE_WHAT_LAUGH_2
            )
        )
        reprompt_text = wrap_with_speak(
            random_build_audio(CAFE_DATE_REPROMPT_1, CAFE_DATE_REPROMPT_2, CAFE_DATE_REPROMPT_3,
                               CAFE_DATE_REPROMPT_4)
        )
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class CafeDateWhereLive(State):
    def next(self, input_action, session, handler_input):
        card_title = "What to order?"
        speech_output = wrap_with_speak(
            random_build_audio(
                CAFE_DATE_WHERE_LIVE_1,
                CAFE_DATE_WHERE_LIVE_2,
                CAFE_DATE_WHERE_LIVE_3
            )
        )
        reprompt_text = wrap_with_speak(
            random_build_audio(CAFE_DATE_REPROMPT_1, CAFE_DATE_REPROMPT_2, CAFE_DATE_REPROMPT_3,
                               CAFE_DATE_REPROMPT_4)
        )
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class CafeDateHowsWeather(State):
    def next(self, input_action, session, handler_input):
        card_title = "What to order?"
        speech_output = wrap_with_speak(
            random_build_audio(
                CAFE_DATE_HOW_IS_WEATHER_1
            )
        )
        reprompt_text = wrap_with_speak(
            random_build_audio(CAFE_DATE_REPROMPT_1, CAFE_DATE_REPROMPT_2, CAFE_DATE_REPROMPT_3,
                               CAFE_DATE_REPROMPT_4)
        )
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class CafeDateLivedWithAnyone(State):
    def next(self, input_action, session, handler_input):
        card_title = "What to order?"
        speech_output = wrap_with_speak(
            random_build_audio(
                CAFE_DATE_LIVED_WITH_SOMEONE_1
            )
        )
        reprompt_text = wrap_with_speak(
            random_build_audio(CAFE_DATE_REPROMPT_1, CAFE_DATE_REPROMPT_2, CAFE_DATE_REPROMPT_3,
                               CAFE_DATE_REPROMPT_4)
        )
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class CafeDateIdealFirstDate(State):
    def next(self, input_action, session, handler_input):
        card_title = "What to order?"
        speech_output = wrap_with_speak(
            random_build_audio(
                CAFE_DATE_IDEAL_FIRST_DATE_1,
                CAFE_DATE_IDEAL_FIRST_DATE_2
            )
        )
        reprompt_text = wrap_with_speak(
            random_build_audio(CAFE_DATE_REPROMPT_1, CAFE_DATE_REPROMPT_2, CAFE_DATE_REPROMPT_3,
                               CAFE_DATE_REPROMPT_4)
        )
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class CafeDateEverBeenInRelationship(State):
    def next(self, input_action, session, handler_input):
        card_title = "What to order?"
        speech_output = wrap_with_speak(
            random_build_audio(
                CAFE_DATE_BEEN_IN_RELATIONSHIP_1,
                CAFE_DATE_BEEN_IN_RELATIONSHIP_2
            )
        )
        reprompt_text = wrap_with_speak(
            random_build_audio(CAFE_DATE_REPROMPT_1, CAFE_DATE_REPROMPT_2, CAFE_DATE_REPROMPT_3,
                               CAFE_DATE_REPROMPT_4)
        )
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)


class CafeDateMarriedOneDay(State):
    def next(self, input_action, session, handler_input):
        card_title = "What to order?"
        speech_output = wrap_with_speak(
            random_build_audio(
                CAFE_DATE_EVER_GET_MARRIED_1,
                CAFE_DATE_EVER_GET_MARRIED_2
            )
        )
        reprompt_text = wrap_with_speak(
            random_build_audio(CAFE_DATE_REPROMPT_1, CAFE_DATE_REPROMPT_2, CAFE_DATE_REPROMPT_3,
                               CAFE_DATE_REPROMPT_4)
        )
        should_end_session = False
        session.set_stored_game_state(None)
        return get_action_response(session, card_title, speech_output, reprompt_text, should_end_session)

