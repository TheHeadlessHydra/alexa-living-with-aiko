"""
All configurations for this instance of the labmda function go here.
"""


class Config(object):
    # ------------------- custom configs -------------------

    session_state_version = "0.0.1"

    # every x utterances it upsells
    upsell_mod = 40

    # the storage type to use
    storage_layer = "DynamoStorage"

    # ------------------- dynamodb storage configs -------------------
    table_name = "alexa_aiko_chan"
    region = "us-east-1"
