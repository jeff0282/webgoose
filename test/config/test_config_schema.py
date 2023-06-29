
"""
webgoose.config (tests) - Test Config Schema

Sanity Check to ensure config schema is not an invalid JSON Schema.
"""

import      json
import      jsonschema

from        webgoose.config     import      SITE_CONFIG_SCHEMA_LOCATION


def test_config_schema_is_valid():

    """
    Uses JSONSchema package to check the config schema.

    If the schema is not valid JSONSchema, this will throw a 
    jsonschema.schema_error
    """

    # Get the schema from file and parse into dict
    with SITE_CONFIG_SCHEMA_LOCATION.open("r", encoding="utf-8") as f:
        schema = json.load(f)

    jsonschema.Validator.check_schema(schema)


