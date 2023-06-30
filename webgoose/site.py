
import      logging
import      jsonschema
import      yaml

from        pathlib                 import      Path
from        typing                  import      Any
from        typing                  import      Dict

from        webgoose.config         import      ConfigUtils
from        webgoose.tree.structs   import      Directory


# Get Logger Instance for this module
logger = logging.getLogger(__name__)


class Site:

    """
    Central object for Webgoose sites.

    Strings together config, tree building, site rendering and export together.
    """

    def __init__(self, config_file_loc: Path) -> None:
        
        """
        Create a site instance using a site.yaml config file.
        """
        self.site_config: Dict[str, Any]


        self.site_config = self.__get_config(config_file_loc)



    def __get_config(self, config_file_loc: Path) -> Dict[str, Any]:
        
        """
        Get site config from site.yaml file.

        Should the config be unreadable, non-existent, or doesn't conform to the schema,
        debugging info will be logged.
        """

        try:
            ConfigUtils.get_config(config_file_loc)

        except FileNotFoundError:
            logger.critical(f"The config file doesn't exist! (file: {config_file_loc.as_posix()})")
            raise SystemExit()

        except yaml.YAMLError as e:
            logger.critical(f"You Have An Error In Your YAML Syntax (file: {config_file_loc.as_posix()})")

            # Print location of error if available
            if hasattr(e, 'problem_mark'):
                mark = e.problem_mark
                logger.critical(f"Error At Line: {mark.line + 1}, Column: {mark.column + 1}")

            raise SystemExit()

        except jsonschema.ValidationError as e:
            logger.critical(f"Your config file is invalid (file: {config_file_loc.as_posix()}) \nReason: {e.message}")
            raise SystemExit()



    def __build_tree(self) -> Directory:
        pass


    def build_site(self):
        pass