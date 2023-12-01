
from    typing      import      Any
from    typing      import      Iterable
from    typing      import      Type

from    ...filelike     import      FileLike



class BaseGroup:
    """
    The base file grouping
    """

    _files: set[Type[FileLike]]

    def __init__(self, initlist: Iterable[Type[FileLike]]) -> None:
        
        # quick duplicate check, if fails try to find what duplicates exist
        fileset = set(initlist)
        if len(fileset) < len(initlist):
            raise FileExistsError("Initial list contains duplicates")
        
        self._files = fileset


    def __bool__(self) -> bool:
        return bool(self._files)
    

    def __contains__(self, cmp: Any) -> bool:
        return cmp in self._files
    


