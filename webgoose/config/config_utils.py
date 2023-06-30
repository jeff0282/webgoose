import      json
import      jsonschema
import      yaml

from        pathlib     import      Path
from        typing      import      Any
from        typing      import      Dict

from        webgoose.config     import      SITE_CONFIG_SCHEMA_LOCATION



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
            - FileNotFoundError:            if config file at path does not exist
            - yaml.YAMLError:               if the config file cannot be parsed by pyyaml
            - jsonschema.ValidationError:   if the config file doesn't adhere to the schema
        """

        # Get config As Dict from YAML File
        config_dict = ConfigUtils.__read_yaml(config_file_path)

        # Validate the above Dict against JSONSchema
        ConfigUtils.validate_against_schema(config_dict)

        # Return resulting dict
        return config_dict
    


    @staticmethod
    def validate_against_schema(config_dict: Dict[str, Any]) -> None:

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



    @staticmethod
    def __read_yaml(config_file_path: Path) -> Dict[str, Any]:

        """
        Get Dict from Yaml File

        Throws FileNotFoundError if the yaml file is not found
        """

        with config_file_path.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file)