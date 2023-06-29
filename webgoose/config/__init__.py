
"""
webgoose.config
---
The config module containing utilities for processing 
and the schema for site.yaml files
"""


# Module Vars
# > Define location of JSONSchema for site.yaml files
from        pathlib     import      Path
SITE_CONFIG_SCHEMA_LOCATION = Path(__file__).parent.joinpath("site_config_schema.json")
DEFAULT_SITE_CONFIG_LOCATION = Path(__file__).parent.joinpath("default_config.yaml")



# Module Imports
from    .config_utils       import      ConfigUtils