
"""
Script Reponsible For Loading Config

(this script is a little weird)


This script must NOT complain if the config file isn't found, as that is the responsibility of other scripts.

Consequently, if the config file isn't found, the script will silently fail and set config = None

If the config file contains errors, the script will silently fail and set config = yaml.YAMLError for later consultation by other scripts

"""

import configparser
import os
import yaml

from typing import Any, Dict, Union



#
# CONSTANTS
#

DEFAULT_CONFIG_PATHS = [".config/config.yaml", "config.yaml"]



def get_config() -> Union[str, None]:

    """
    Attempts To Get The Config File From A Few Potential Locations

    If It Manages To Get It, Pass It To parse_config() And Return Whatever It Returns, Otherwise Return None
    """

    for path in DEFAULT_CONFIG_PATHS:

        try:

            with open(path, "r", encoding="utf-8") as raw_config:
                return yaml.safe_load(raw_config)
        
        except (FileNotFoundError, IOError):

            continue

        except yaml.YAMLError as e:

            return e

        
        # If No Config File Found, Return None
        return None




config = get_config()