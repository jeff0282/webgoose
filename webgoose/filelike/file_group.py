
from    typing      import      Iterable
from    typing      import      Type
from    typing      import      NewType
from    typing      import      Union

from    .           import      BaseFile
from    .           import      FileLike


class FileGroup(FileLike):
    """
    Base class for FileLikes that act as 'Directories'

    FileLike 'Directories' are less directories and more groupings,
    as children can have multi-level names (i.e. path/to/file.txt)
    """

    class DirListing:
        """
        A FileListing Used Internally for DirNodes
        """

        DirListingItem = dict[str, Type[BaseFile] | Type['FileGroup.DirNode']]
        _children = DirListingItem


        def __init__(self) -> None:
            self._children = dict()


        def __contains__(self, cmp: str | DirListingItem) -> bool:
            if isinstance(cmp, (BaseFile, FileGroup.DirNode)):
                return cmp in self._children.values()

            elif isinstance(cmp, str):
                cmp = cmp.casefold()
                return cmp in self._children

            return False


        def add(self, filename: str, file_obj: DirListingItem) -> None:
            filename = filename.casefold()
            if filename in self._children:
                raise FileExistsError(f"Duplicate Filename: '{filename}' exists")
            
            self._children[filename] = file_obj


        def pop(self, filename: str) -> DirListingItem:
            filename = filename.casefold()
            try:
                return self._children.pop(filename)
            
            except KeyError as e:
                raise FileNotFoundError(f"Filename not found: '{filename}' doesn't exist in this Listing") from e
            

        def get(self, filename: str) -> DirListingItem:
            filename = filename.casefold()
            try:
                return self._children[filename]
            
            except KeyError as e:
                raise FileNotFoundError(f"Filename not found: '{filename}' doesn't exist in this Listing") from e


    
    class DirNode:
        pass
    

    def __init__(self) -> None:
        """
        Create an empty FileGroup instance
        """



    