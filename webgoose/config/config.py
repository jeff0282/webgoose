
import      yaml

from        pathlib     import      Path
from        typing      import      Any
from        typing      import      Dict


SITE_CONFIG_SCHEMA_LOCATION = Path(__file__).parent.joinpath("site_config_schema.json")



class Config:


    @staticmethod
    def get_config(config_file_path: Path) -> Dict[str, Any]:

        """
        Get and parse site.yaml file into a Dict. Performs type checks
        against a JSON Schema.
        """

        config_dict = Config.__read_yaml(config_file_path)
        
        try:
            Config.__validate_against_schema(config_dict)

        except:




    @staticmethod
    def __read_yaml(config_file_path: Path) -> Dict[str, Any]:

        """
        Get Dict from Yaml File
        """

        with config_file_path.open("r") as file:
            return yaml.safe_load(file)
        

    @staticmethod
    def __validate_against_schema():