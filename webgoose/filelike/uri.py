
import  os

from    typing      import      Iterator
from    typing      import      Type

from    pathlib         import      PureWindowsPath
from    pathlib         import      PurePosixPath
from    pathvalidate    import      ValidationError
from    pathvalidate    import      validate_filepath

from    .               import      InvalidURIError


class URI:
    """
    A tuple-like implementation of URIs
    """
    
    # ---
    # Class Attrs
    # This class uses exlusively posix paths internally, so
    # we cannot rely on os.path
    path_sep = "/"
    ext_sep = "."

    # ---
    # Instance Typing
    _slug_tuple: tuple[str, ...]


    def __init__(self, *slug_parts: str | os.PathLike | Type['URI']):
        """
        Create a slug instance with one or more string or PathLike objects

        Strings and PathLike objects can be mixed provided they create a valid URI

        If multiple absolute paths provided, uses the last one.
        """

        # Validate Posix Path, Ensure all slug_parts are strings
        # (Create windows path and convert to posix to ensure any invalid drive letters, etc are picked up)
        str_posix_path = PureWindowsPath(*(str(part) for part in slug_parts)).as_posix()
        try:
            validate_filepath(str_posix_path, "POSIX")

        except ValidationError as ve:
            raise InvalidURIError("Path provided is not a valid POSIX path") from ve

        # Use PurePosixPath to split path into tuple
        # Ensure that no parts of the path contain parent dir refs
        parts = PurePosixPath(str_posix_path).parts
        if any(part for part in parts if part == os.pardir):
            raise InvalidURIError(f"Path must not contain any parent directory references")
        
        # if all good, set parts
        self._slug_tuple = parts


    def __repr__(self) -> str:
        """
        Return the definitive string form of this slug
        """

        # handle absolute slug
        # if instance is absolute, use first element as prefix 
        # and join remainder by Slug.path_sep
        if self.is_absolute:
            return self[0] + self.path_sep.join(self[1:])
        
        # otherwise, slug is absolute
        return self.path_sep.join(self)


    def __str__(self) -> str:
        """
        Return the string form of this slug
        """

        return repr(self) 
    

    def __bool__(self) -> bool:
        return bool(self._slug_tuple)
    

    def __add__(self, to_add: Type['URI'] | str | os.PathLike) -> Type['URI']:
        """
        Allow conjugation of Slugs using the addition operator
        """
        
        # create a new slug object out of this and the other instance
        if isinstance(to_add, (URI, str, os.PathLike)):
            return self.__class__(self, to_add)

        return NotImplemented
    

    def __radd__(self, to_add: str) -> Type['URI']:
        """
        Allow reverse conjugation of strings to Slug instances using addition operator
        """

        # create new slug object using string
        if isinstance(to_add, (str, os.PathLike)):
            return self.__class__(to_add, self)

        return NotImplemented
    

    def __contains__(self, cmp: str) -> bool:
        """
        Allow contains checks for string parts

        If instance is absolute, first item ignored for comparison
        """

        return cmp in self[1:] if self.is_absolute else cmp in self
    

    def __len__(self) -> int:
        return len(self._slug_tuple)
    

    def __hash__(self) -> int:
        """
        Hash by this file's slug tuple
        """

        return hash(self._slug_tuple)
    

    def __eq__(self, cmp: str | Type['URI']) -> bool:
        """
        Allow equality checks using strings or slug instances
        """
        
        # if cmp is a string, attempt to make a slug out of it
        # and compare it to this instance
        if isinstance(cmp, str):
            try:
                return hash(self) == hash(self.__class__(cmp))
            except:
                return False

        # if cmp is already a slug instance, do a straight hash comparison
        elif isinstance(cmp, URI):
            return hash(self) == hash(cmp)
        
        # if no matches type match above, then not equal
        return False
    

    def __iter__(self) -> Iterator[str]:
        """
        Allow iterating through slugs by each path item
        """

        for part in self._slug_tuple:
            yield part


    def __getitem__(self, key: int | slice) -> str | Type['URI']:
        """
        Implement slug access by index and slicing
        """

        # if slice requested, create a new slug with sliced slug tuple
        if isinstance(key, slice):
            return self.__class__(*(self._slug_tuple[i] for i in range(*key.indices(len(self._slug_tuple)))))
        
        # if int key requested, get the index from slug tuple, return as string
        elif isinstance(key, int):
            return self._slug_tuple[key]
        
        # if not slice or int, key is invalid
        raise TypeError(f"Invalid Key Type: Expected 'slice' or 'int', recieved '{type(key)}'")
    

    @property
    def is_absolute(self) -> bool:
        """
        True if path is absolute, false otherwise
        """
        return self[0] == self.path_sep
        
    
    @property
    def filename(self) -> str:
        """
        This slug's filename as a string
        """

        # slug may be empty
        if self:
            return self[-1]
        
        return ""
    

    @property
    def dirname(self) -> Type['URI']:
        """
        Return this URI one level up as a new URI instance
        """

        # slicing returns a new URI instance
        return self[:-1]
    

    @property
    def basename(self) -> str:
        """
        This slug's basename as a string (the filename stripped of extensions)
        """

        try:
            i = self.filename.index(os.extsep, 1)
            return self.filename[:i]
        
        except ValueError:
            return self.filename


    @property
    def ext(self) -> str:
        """
        This slug's extensions as a string

        i.e.
        ```
        file_no_exts -> ''
        file.txt -> '.txt'
        .hidden.txt -> '.txt'
        archive.tar.gz -> '.tar.gz'
        ```
        """

        try:
            i = self.filename.index(self.ext_sep, 1)
            return self.filename[i:]

        except:
            return ""
        

    @property
    def exts(self) -> tuple[str, ...]:
        """
        Returns a slug's extensions as a tuple of strings,
        excluding dots.

        i.e.
        ```
        file_no_exts -> ()
        archive.tar.gz -> ('tar', 'gz')
        ```
        """
        if self.ext:
            # chop off first seperator, then split by the seperator
            ext = self.ext[1:]
            return tuple(ext.split(self.ext_sep))

        # otherwise return empty tuple
        return tuple()