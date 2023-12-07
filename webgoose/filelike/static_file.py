
import  os

from    pathlib     import      Path

from    .           import      BaseFile


class StaticFile(BaseFile):
    """
    Abstract Class for Static Files

    Mandates the `source` property, which should be a Path object
    linking back to the source file
    """

    def __init__(self, path: os.PathLike | str) -> None:
        """
        Create a Static File object using a string-path or pathlike object
        """
        self._source = Path(path)


    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{str(self.source)}')"
    
    def __str__(self) -> str:
        return str(self.source)
    
    @property
    def source(self) -> Path:
        return self._source
