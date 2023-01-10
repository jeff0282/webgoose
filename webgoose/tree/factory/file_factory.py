
from    pathlib     import      Path
from    typing      import      Any
from    typing      import      Dict

from    tree.struct import      File

class FileFactory:

    """
    File Factory
    ---

    Grabs all the information about a file using it's corresponding Path Object,
    Builds an immutable object containing all of this information for the User's
    comvenience.
    """


    def __init__(self, file_path: Path) -> None:

        """
        Initalises The Instance with the Path Object for Future Use
        """

        self.__source = file_path



    def build(self) -> File:

        """
        Grabs all file information using the methods listed here, and 
        uses them to initialise a File Object.
        """

        file_info = self._get_file_info()
        return File(file_info['basename'],
                    file_info['ext'],
                    file_info['last_mod'])



    def _get_file_info(self) -> Dict[str, Any]:

        """
        Retrieve Basic File Metadata and Return As Dictionary
        """

        file_info = dict()

        file_info['basename'] = self.__source.stem
        file_info['ext'] = self.__source.suffix
        file_info['last_mod'] = self.__source.stat().st_mtime 

        return file_info