
import configparser
import os
import sys
import yaml


# Relative Location From CWD
DEFAULT_CONFIG_LOCATION = ".config/config.yaml"

if os.path.isfile(DEFAULT_CONFIG_LOCATION):

    with open(DEFAULT_CONFIG_LOCATION, "r", encoding="utf-8") as raw_config:
        try:

            config = yaml.safe_load(raw_config)

        except yaml.YAMLError as e:

            # Exit As Nothing Can Be Done If Config Can't Be Loaded
            # Try and Get Error Info From YAML To Display To User
            err_str = "FATAL: Incorrectly Formatted Config File:\nPlease Check Your Config File For Syntax Errors"

            # This Is Taken From Python-YAML Documentation (idk why you need +1 for lines and columns)
            if hasattr(e, 'problem_mark'):
                mark = e.problem_mark
                err_str += f"\nError At Line: {mark.line+1}, Column: {mark.column+1}"

            sys.exit(err_str)

else:

    # Exit As Nothing Can Be Done, Print Error To STDERR
    sys.exit(f"FATAL: Unable To Open Config File:\nThe Config File, Located at Path '{DEFAULT_CONFIG_LOCATION}', Either Doesn't Exist or is Inaccessable")