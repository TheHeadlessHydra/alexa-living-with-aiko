"""
This is the schema of the state of a player.
This is passed along between sessions and stored in an external persistence layer between calls.

It is very important to be careful when changing anything in this schema. The state is stored externally in DynamoDB.
It is highly likely that production code will break if non-backwards-compatible changes are made. Therefore, make sure
everything that is changed is backwards compatible. If you need to make a non-backwards compatible change,
session_state_builder has a method for handling non-backwards-compatible changes called session_state_schema_converter.

The serialize and deserialize methods will optimize the writes of each individual object in the state.
If changes need to be made to the schema, the serialize and deserialize methods need to be changed to reflect the changes.
Make sure to compact and compress the final result as best as possible to save on storage costs. This is the reason we
do not simple pickle the entire Session object.
"""

from config import *
from enum import Enum


class Session(object):
    def __init__(self, session_state):
        self.user_id = self.set_user_id_deserialize(session_state)
        self.first_time_user = self.set_first_time_user_deserialize(session_state)
        self.stored_game_state = self.set_stored_game_state_deserialize(session_state)
        self.previous_game_state = self.set_previous_stored_game_state_deserialize(session_state)
        self.voice_mode = self.set_voice_mode_deserialize(session_state)
        self.is_in_cafe_date = self.set_is_in_cafe_date_deserialize(session_state)
        self.total_number_of_utterances = self.set_total_number_of_utterances_deserialize(session_state)

        # Decorators used throughout the code but not commited to session state
        self.is_tsundere_mode_purchased = None
        self.is_cafe_date_purchased = None
        self.is_tsundere_mode_purchasable = None
        self.is_cafe_date_purchasable = None

    # -------------------- SessionState builder --------------------
    def get_session_state(self):
        session_state = SessionState(self.get_user_id_serializable())
        session_state.first_time_user = self.get_first_time_user()
        session_state.stored_game_state = self.get_stored_game_state_serializable()
        session_state.previous_game_state = self.get_previous_stored_game_state_serializable()
        session_state.voice_mode = self.get_voice_mode_serializable()
        session_state.is_in_cafe_date = self.get_is_in_cafe_date()
        session_state.total_number_of_utterances = self.get_total_number_of_utterances()
        return session_state

    # -------------------- user id --------------------
    def get_user_id_serializable(self):
        return self.user_id

    def set_user_id_deserialize(self, session_state):
        return session_state.user_id

    # -------------------- first time user --------------------
    def get_first_time_user(self):
        return self.first_time_user

    def set_first_time_user(self, first_time_user):
        self.first_time_user = first_time_user

    def get_first_time_user_serializable(self):
        return self.first_time_user

    def set_first_time_user_deserialize(self, session_state):
        return session_state.first_time_user

    # -------------------- game state --------------------
    def get_stored_game_state(self):
        return self.stored_game_state

    def set_stored_game_state(self, stored_game_state):
        self.stored_game_state = stored_game_state

    def get_stored_game_state_serializable(self):
        return self.stored_game_state

    def set_stored_game_state_deserialize(self, session_state):
        return session_state.stored_game_state

    # -------------------- total number of utterances --------------------
    def get_total_number_of_utterances(self):
        return self.total_number_of_utterances

    def set_total_number_of_utterances(self, total_number_of_utterances):
        self.total_number_of_utterances = total_number_of_utterances

    def get_total_number_of_utterances_serializable(self):
        return self.total_number_of_utterances

    def set_total_number_of_utterances_deserialize(self, session_state):
        return session_state.total_number_of_utterances

    # -------------------- previous game state --------------------
    def get_previous_stored_game_state(self):
        return self.previous_game_state

    def set_previous_stored_game_state(self, previous_game_state):
        self.previous_game_state = previous_game_state

    def get_previous_stored_game_state_serializable(self):
        return self.previous_game_state

    def set_previous_stored_game_state_deserialize(self, session_state):
        return session_state.previous_game_state

    # -------------------- voice mode --------------------
    def get_voice_mode(self):
        return self.voice_mode

    def set_voice_mode(self, voice_mode):
        self.voice_mode = voice_mode

    def get_voice_mode_serializable(self):
        return self.voice_mode.value

    def set_voice_mode_deserialize(self, session_state):
        return VoiceMode(session_state.voice_mode)

    # -------------------- is in cafe date --------------------
    def get_is_in_cafe_date(self):
        return self.is_in_cafe_date

    def set_is_in_cafe_date(self, is_in_cafe_date):
        self.is_in_cafe_date = is_in_cafe_date

    def get_is_in_cafe_date_serializable(self):
        return self.is_in_cafe_date

    def set_is_in_cafe_date_deserialize(self, session_state):
        return session_state.is_in_cafe_date

    # -------------------- decorators --------------------
    def get_is_tsundere_mode_purchased(self):
        return self.is_tsundere_mode_purchased

    def get_is_cafe_date_purchased(self):
        return self.is_cafe_date_purchased

    def get_is_tsundere_mode_purchasable(self):
        return self.is_tsundere_mode_purchasable

    def get_is_cafe_date_purchasable(self):
        return self.is_cafe_date_purchasable

    def set_is_tsundere_mode_purchased(self, is_tsundere_mode_purchased):
        self.is_tsundere_mode_purchased = is_tsundere_mode_purchased

    def set_is_cafe_date_purchased(self, is_cafe_date_purchased):
        self.is_cafe_date_purchased = is_cafe_date_purchased

    def set_is_tsundere_mode_purchasable(self, is_tsundere_mode_purchasable):
        self.is_tsundere_mode_purchasable = is_tsundere_mode_purchasable

    def set_is_cafe_date_purchasable(self, is_cafe_date_purchasable):
        self.is_cafe_date_purchasable = is_cafe_date_purchasable

    # -------------------- reset state --------------------

    def restart_session(self):
        self.stored_game_state = None
        self.previous_game_state = None


class VoiceMode(Enum):
    ORIGINAL = 1
    DERE = 2
    TSUNDERE = 3


class SessionState(object):
    """The object that gets serialized and deserialized to storage. It has been stripped down to its bare essentials
    to save on storage costs. The serialize and deserialize methods above handle the conversion from the storage
    format to the Session object.
    """

    def __init__(self, user_id):
        self.user_id = user_id

        # If the player is a first time player
        self.first_time_user = True

        # Where the player is, indicated by the ClassName of the state in the StateMachine.
        self.stored_game_state = None

        # Where the player was last, indicated by the ClassName of the state in the StateMachine.
        self.previous_game_state = None

        # What voice mode
        self.voice_mode = VoiceMode.DERE

        # Is currently in a cafe date
        self.is_in_cafe_date = None

        # Total number of utterances used to track upsell
        self.total_number_of_utterances = 0

        # The version of this schema
        self.version = Config.session_state_version
