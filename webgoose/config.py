
import configparser

# Relative Location From CWD
DEFAULT_CONFIG_LOCATION = ".config/config.ini"

# Get Config Stuffs
config = configparser.ConfigParser()
config.read(DEFAULT_CONFIG_LOCATION)