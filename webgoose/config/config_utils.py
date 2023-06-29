import      json
import      jsonschema
import      yaml

from        pathlib     import      Path
from        typing      import      Any
from        typing      import      Dict

from        webgoose.exceptions     import      WebgooseException


# Set 'Constant' Location of Site Config Schema
# > Should be located in the same directory as this module.
SITE_CONFIG_SCHEMA_LOCATION = Path(__file__).parent.joinpath("site_config_schema.json")


class MalformedConfigError(WebgooseException):
    """Site Config File is unable to be parsed, or does not
    conform to the site.yaml schema."""
    pass



class ConfigUtils:

    """
    Utility class for reading and validating Site.yaml files used
    for the configuration of the site.
    """


    @staticmethod
    def get_config(config_file_path: Path) -> Dict[str, Any]:

        """
        Get and parse site.yaml file into a Dict. Performs type checks
        against a JSON Schema.

        MAY THROW THE FOLLOWING EXCEPTIONS:
            - FileNotFoundError:    if config file at path does not exist
            - MalformedConfigError: if config cannot be parsed or does not adhere to schema
        """

        try:
            # Get config As Dict from YAML File
            # NOTE: FileNotFoundError is __NOT__ handled here
            config_dict = ConfigUtils.__read_yaml(config_file_path)

            # Validate the above Dict against JSONSchema
            ConfigUtils.__validate_against_schema(config_dict)

        except yaml.YAMLError as yaml_error:
            raise MalformedConfigError from yaml_error

        except jsonschema.ValidationError as json_error:
            raise MalformedConfigError from json_error
        
        # If the above all checks out, return the config dict
        return config_dict




    @staticmethod
    def __read_yaml(config_file_path: Path) -> Dict[str, Any]:

        """
        Get Dict from Yaml File

        Throws FileNotFoundError if the yaml file is not found
        """

        with config_file_path.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file)
        

    @staticmethod
    def __validate_against_schema(config_dict: Dict[str, Any]) -> None:

        """
        Validate a provided site.yaml as a Dict against a JSON schema.

        Checks for types and required values. 

        This is __NOT__ a guarantee the the schema is perfectly good, as
        the provided dict may not provide all necessary parameters for a 
        tree builder, for instance.

        Throws a jsonschema.ValidationError if the dict fails to conform to the schema.
        """

        # Get the schema from file.
        with SITE_CONFIG_SCHEMA_LOCATION.open("r", encoding="utf-8") as schema_file:
            schema = json.load(schema_file)

        jsonschema.validate(config_dict, schema=schema)