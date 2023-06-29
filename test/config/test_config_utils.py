
"""
webgoose.config (tests) - Test Config Utils

Ensure that site.yaml files are parsed and validated correctly
"""

import  pytest

from    webgoose.config     import      ConfigUtils
from    webgoose.config     import      DEFAULT_SITE_CONFIG_LOCATION


def test_default_config():

    """
    Attempt to get, parse, and validate the default site.yaml file

    No exceptions should be raised
    """

    config = ConfigUtils.get_config(DEFAULT_SITE_CONFIG_LOCATION)

    # This is pretty much pointless, but who cares
    assert type(config) == dict