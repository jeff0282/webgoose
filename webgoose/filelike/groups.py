
from    typing          import      Iterable
from    typing          import      Iterator
from    typing          import      Type

from    dataclasses     import      dataclass

from    .               import      FileLike
from    .               import      URI


class FileList:
    """
    A list-like structure for storing attachted file-like objects

    Provides a variety of methods for retrieving file-likes and creating
    subsets.
    """

    @dataclass
    class DirNode:
        """
        A little dataclass for storing directory contents
        """
        files: list[Type[FileLike]]     = []
        index: Type[FileLike] | None    = None

        @property
        def all(self) -> tuple[Type[FileLike]]:
            """
            Return every file in this directory, including index
            """

            if self.index:
                return [*self.files, self.index]
            return (*self.files,)


    # Full Mapping
    # Contains all file and directory information
    _full_mapping: dict[Type[URI], Type[DirNode]]


    def __init__(self, initlist: Iterable[Type[FileLike]] = None) -> None:
        """
        Create an FileList
        """
        self._full_mapping = {URI(""): FileList.DirNode()}
        if initlist:
            self.extend(*initlist)


    def __repr__(self) -> str:
        """
        Official representation as string
        """

        return f"{self.__class__.__name__}([{', '.join(self)}])"


    def __str__(self) -> str:
        """
        String formatted representation
        """

        return repr(self)
    

    def __bool__(self) -> bool:
        """
        Returns True if this FileList contains anything, false otherwise
        """

        return bool(self._full_mapping) or bool(self._index_mapping)
    

    def __iter__(self) -> Iterator[Type[FileLike], None, None]:
        """
        Allow iteration over this FileList
        """

        # extract all directory listings into a single, flat iterable
        return iter(file for files in self._full_mapping.values() for file in files)
    

    def __contains__(self, cmp: str | Type[URI] | Type[FileLike]) -> bool:
        """
        Check if this FileList contains a given entry

        If given a string or URI: checks if that paths exists
        If given a FileLike: do above with FileLike slug, check if match is same object
        """

        return bool(self.get(cmp))
        

    def get(self, file_to_get: str | Type[URI] | Type[FileLike]) -> Type[FileLike]:
        """
        Get a FileLike from this FileList using either a string URI, URI instance,
        or reference to a FileLike object
        """

        match = None
        search_uri = file_to_get
        ref_matching = False

        if isinstance(file_to_get, str):
            search_uri = URI(file_to_get)

        elif isinstance(file_to_get, FileLike):
            ref_matching = True
            search_uri = file_to_get.uri

        # if type is or has been transformed into a URI, perform search
        if isinstance(search_uri, URI):
            # see if search_uri is for a directory index
            dir = self._full_mapping.get(search_uri, None)
            if dir:
                if dir.index:
                    return dir.index
            
            # otherwise, attempt to get dirname of search uri, see if it contains basename (the file we're after)
            else:
                dir = self._full_mapping.get(search_uri.dirname, None)
                if dir:
                    match = next(file for file in dir.all if file.basename == search_uri.basename)
        
        # if match is not None, we've found something
        # perform ref_matching if necessary, otherwise return match if set
        if match:
            if ref_matching:
                if match is file_to_get:
                    return match
            return match

        # if we get here, file doesn't exist
        raise FileNotFoundError(f"File Not Found: FileLike '{file_to_get}' does not exist in this FileList")
    

    # TODO: IMPLEMENT ADD, EXTEND, CONFLICTS_WITH, ETC