
# Initialise Version Information
version_info = (0, 0, 2)
version = '.'.join(str(c) for c in version_info)


# Get Config Stuffs
import configparser
config = configparser.ConfigParser()
config.read(".config/config.ini")