"""
The LaunchRequest is unique in that it must launch the first world. To avoid circular dependencies, it must be isolated
from the common state machine classes.

This file also holds are initializer helper methods used to start the state machine.
"""

from game import *
from state import *
from cannot_build_state_machine_exception import *
from state_machine_helpers import *
from state_machine_at_home import *
from state_machine_isp import *
from state_machine_cafe_date import *
from state_machine_common import *
import sys


class LaunchRequest(State):
    """This is the beginning of the entire game for a user. For now, we start at the piranha paradise visitor center.
    """

    def next(self, input_action, session_state, handler_input):
        return HomeIdleState().next(input_action, session_state, handler_input)


# --------------- State Machine Initializers ------------------

def build_state_machine_from_source(source, user_id=None, session=None):
    print("Initializing state machine with specified source {} and state: {}".format(str(source), str(session)))

    try:
        if session is not None:
            state_object = initialize_game(source, session)
        elif user_id is not None:
            state_object = initialize_game(source, Session(SessionState(user_id)))
        else:
            raise Exception("One of user_id or session needs to be available to generate new session")
    except Exception as e:
        # Since we are specifying where to start from, if this is wrong, then it is a logic bug
        print(e)
        message = "Unexpected error getting state machine from SessionState: " + str(sys.exc_info()[0])
        print(message, sys.exc_info()[0])
        raise CannotBuildStateMachineException(message)
    return state_object


def rebuild_state_machine_from_session(input_action, session):
    print("Initializing state machine with stored session state")

    try:
        print(session)
        stored_game_state = session.get_stored_game_state()
        if stored_game_state is None:
            print("Stored game state is empty, initializing game state from scratch.")
            return initialize_new_state_machine_from_input(input_action, session=session)
        print("Restoring game at state: " + str(stored_game_state))
        return initialize_game(stored_game_state, session)
    except Exception as e:
        # Since it is being restored from state, if this fails with an exception, then we have a logic bug. The state
        # should never have a bad restore point.
        print(e)
        message = "Unexpected error getting state machine from SessionState: " + str(sys.exc_info()[0])
        print(message, sys.exc_info()[0])
        raise CannotBuildStateMachineException(message)


def initialize_new_state_machine_from_input(input_action, user_id=None, session=None):
    print("Initializing state machine with with no stored session state, but with input: " + str(input_action))

    try:
        print("Converting " + input_action + " to class")
        if session is not None:
            state_object = initialize_game(input_action, session)
        elif user_id is not None:
            state_object = initialize_game(input_action, Session(SessionState(user_id)))
        else:
            raise Exception("One of user_id or session needs to be available to generate new session")
    except Exception as e:
        # There are certain intents that can be triggered that do not map directly. We do not want to crash on those.
        # Give a not understood response back.
        print(e)
        message = "Unexpected error converting " + str(input_action) + " to a class." + str(sys.exc_info()[0])
        print(message, sys.exc_info()[0])
        state_object = Game(NotUnderstood(), session)
    return state_object


def initialize_game(state, session):
    # If in the middle of a cafe date, and user tries to do a non-cafe date intent, return not understood
    if session.get_is_in_cafe_date() and not state.startswith('CafeDate'):
        return Game(NotUnderstoodCafeDate(), session)
    return Game(globals()[state](), session)
