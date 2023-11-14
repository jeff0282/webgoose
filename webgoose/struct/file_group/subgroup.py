
import  os

from    typing      import      Any
from    typing      import      Type

from    collections     import      UserList
from    wcmatch         import      glob

from    webgoose.struct     import      FileGroup



class BaseSubgroup(UserList):

    """
    The base subgroup for components

    Groupings are simply lists with extra stuff attached

    Keeps a dict with str keys as the new relative paths for the files,
    mapped to the objects that represent the files

    Implements some basic methods for creating subgroups
    """

    _file_cls: Type[BaseFile] = BaseFile
    parent_group: Type[FileGroup]
    data: list[_file_cls]


    def __init__(self, 
                 initlist: Optional[list[Type[_file_cls]]] = None,
                 *, 
                 parent_group: Type['FileGroup']) -> None:
        """
        Create a BaseSubgroup object.

        Not for direct use; to be inherited from
        """

        self._parent_group = parent_group
        initlist = initlist if initlist else []

        super().__init__(initlist, parent_group=parent_group)


    #
    # PREVENT DELETION
    def remove(self, _ = None):
        raise RuntimeError("Deletion not allowed")
         

    #
    # PREVENT DELETION
    def pop(self, _ = None):
        raise RuntimeError("Deletion not allowed")


    def glob(self, pattern: str) -> Type['BaseSubgroup']:
        """
        Get all files that match a given pattern

        Returns a new grouping containing the subset of files
        """
        
        matches = []
        for file in self:
            if glob.globmatch(file.slug, pattern):
                matches.append(file)

        return self.__class__(matches, parent_group=self._parent_group)

    
class StaticSubgroup(BaseSubgroup):

    """
    A subgroup specifically for static files.

    Takes os.PathLike objects as its file representation, 
    stores (coverts if necessary) as pathlib.Path objects
    """
    
    _file_cls = StaticFile

    def __setitem__(self, 
                    i: int, 
                    path: str, 
                    obj: str | os.PathLike | Type[_file_cls]) -> None:

        # ADDS SOME LOGIC TO ALLOW ADDITION OF STATICFILES BY PATHLIKE OBJECTS & STRS
        # if object provided is a pathlike or string, convert to a static file object
        # otherwise, assume obj is a staticfile obj
        if isinstance(obj, os.PathLike) or type(obj) == str:
            obj = self._file_cls(obj)

        self.data[i] = obj


class RenderSubgroup(BaseSubgroup):

    """
    A subgroup for Renderable objects.

    Extends the BaseSubgroup by adding additional methods 
    for handling Renderables (grouping by metadata, etc).
    """

    _file_cls = Renderable

    #TODO: ADD METHODS FOR GROUPING BY RENDERABLES META, ETC