
import  os
import  re

from    typing      import      Iterable
from    typing      import      Iterator
from    typing      import      Type

from    pathvalidate    import      ValidationError
from    pathvalidate    import      validate_filepath

from    .               import      InvalidURIError


class URI:
    """
    A tuple-like implementation of URIs
    """
    
    # ---
    # Class Attrs
    # This class uses exlusively posix paths internally, so we cannot rely on os.path
    # path seperators are assumed internally to only be one char long
    # NOTE: `input_sep` are alternative seperators recognised for ONLY input paths
    path_sep = "/"
    input_seps = (path_sep, "\\\\") # balls
    ext_sep = "."

    # ---
    # Instance Typing
    _uri_parts: tuple[str, ...]


    def __init__(self, *path_parts: str | os.PathLike | Type['URI']):
        """
        Create a URI instance with one or more string, PathLike or URI instances

        If multiple absolute paths provided, uses the last one. Supports trailing slashes.

        Raises InvalidURIError if path(s) provided creates an invalid URI
        """ 

        # split and extract info from provided path(s)
        parts, is_abs, is_dir = self.create_uri_parts(path_parts)
        self._is_abs = is_abs
        self._is_dir = is_dir
        self._uri_parts = parts


    def __repr__(self) -> str:
        """
        Return the definitive REPR string form of this URI
        """

        return f"{self.__class__.__name__}('{str(self)}')"


    def __str__(self) -> str:
        """
        Return the string form of this URI
        """

        return self.parts_to_string(self.parts, is_abs=self.is_absolute, is_dir=self.is_dir)
    

    def __bool__(self) -> bool:
        return bool(repr(self))
    

    def __add__(self, to_add: Type['URI'] | str | os.PathLike) -> Type['URI']:
        """
        Allow conjugation of URIs using the addition operator
        """
        
        # create a new URI instance out of this and another string, pathlike or URI
        if isinstance(to_add, (URI, str, os.PathLike)):
            return self.__class__(self, to_add)

        return NotImplemented
    

    def __radd__(self, to_add: str) -> Type['URI']:
        """
        Allow reverse conjugation of strings to Slug instances using addition operator
        """

        # create new URI object using string or pathlike
        if isinstance(to_add, (str, os.PathLike)):
            return self.__class__(to_add, self)

        return NotImplemented
    

    def __contains__(self, cmp: str) -> bool:
        """
        Allow contains checks for string parts

        If instance is absolute, first item ignored for comparison
        """

        return cmp in self.parts
    

    def __len__(self) -> int:
        return len(self.parts)
    

    def __hash__(self) -> int:
        """
        Hash by this URI's parts and is_absolute status

        NOTE:   is_dir status is NOT considered for hashing
                to allow /path/to/dir == /path/to/dir/
        """

        return hash((self.is_absolute, self.parts))
    

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

        return iter(self.parts)


    def __getitem__(self, key: int | slice) -> str | Type['URI']:
        """
        Implement slug access by index and slicing
        """

        # if slice requested, create a new slug with sliced slug tuple
        if isinstance(key, slice):
            return self.__class__(*(self.parts[i] for i in range(*key.indices(len(self.parts)))))
        
        # if int key requested, get the index from slug tuple, return as string
        elif isinstance(key, int):
            return self.parts[key]
        
        # if not slice or int, key is invalid
        raise TypeError(f"Invalid Key Type: Expected 'slice' or 'int', recieved '{type(key)}'")
    

    @property
    def is_absolute(self) -> bool:
        """
        True if URI is absolute, false otherwise
        """

        return self._is_abs
    

    @property
    def is_dir(self) -> bool:
        """
        True if URI is a directory (ends with slash), false otherwise
        """

        return self._is_dir
    

    @property
    def parts(self) -> tuple[str, ...]:
        """
        Return this URIs string parts as a tuple

        Resultant tuple does NOT include start of end slashes,
        regardless of whether URI is absolute or is a dir
        """

        return self._uri_parts
        
    
    @property
    def basename(self) -> str:
        """
        This last component of the URI
        """

        # slug may be empty
        if self.parts:
            return self[-1]
        
        return ""
    

    @property
    def dirname(self) -> Type['URI']:
        """
        Return this URI one level up as a new URI instance
        """

        # ensure returned URI instance is recognised as a dir
        return self.__class__(self[:-1] + self.path_sep)
    

    @property
    def stem(self) -> str:
        """
        This URI's basename stripped of extensions
        """

        try:
            i = self.basename.index(os.extsep, 1)
            return self.basename[:i]
        
        except ValueError:
            return self.basename


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
            i = self.basename.index(self.ext_sep, 1)
            return self.basename[i:]

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
    

    def parts_to_string(self, parts: tuple[str, ...], *, is_abs: bool = False, is_dir: bool = False) -> str:
        """
        Convert tuple of strings into a string path

        Additional Params:
        - `is_abs`: adds leading slash to resultant path
        - `is_dir`: adds trailing slash to resultant path 
        """

        # if absolute, add path sep to start
        # if dir, add path sep to end
        uri_str = self.path_sep.join(parts)
        if is_abs:
            uri_str = self.path_sep + uri_str

        # only add trailing slash if path contains stuff
        if is_dir and parts:
            uri_str = uri_str + self.path_sep

        return uri_str
    

    def validate_uri_parts(self, parts: tuple[str, ...], *, is_abs: bool = False, is_dir: bool = False) -> str:
        """
        Validates provided URI parts

        Raises InvalidURIError on error
        """

        path = self.parts_to_string(parts, is_abs=is_abs, is_dir=is_dir)
        # > check for parent dir references
        if os.pardir in parts:
            raise InvalidURIError(f"URI may not contain parent dir references '{os.pardir}'. Path Provided '{path}'")
        
        # > validate filepath for POSIX compliance
        try:
            validate_filepath(path, "POSIX")
        except ValidationError as e:
            raise InvalidURIError(f"Path(s) provided do not form a valid URI. Path provided '{path}'; Reason: {e.reason}") from e


    def create_uri_parts(self, _iterable: str | os.PathLike | Type['URI']) -> tuple[tuple[str, ...], bool, bool]:
        """
        Takes an iterable of Strings, Pathlike or URI objects and converts them into suitable format 
        the creation of a URI instance.

        Returns a tuple in the form:
        - `path parts`: tuple[str, ...];    the individual names of each part of the final path as a tuple,
        - `is_abs`: bool;                   True if the final path is absolute, False otherwise,
        - `is_dir`: bool;                   True if the final path is a dir (trailing slash), False otherwise.
        """

        is_abs = False
        is_dir = False
        parts = []

        # iterate over the provided path components in reverse
        # (faster in the case where provided components contains multiple absolute paths)
        first_iter = True
        split_pattern = re.compile(fr"{'|'.join(self.input_seps)}") # fr fr ong
        for path_part in reversed(_iterable):
            path_part = str(path_part)

            # if we're on first iteration (last element) check for trailing slash
            if first_iter:
                first_iter = False

                # if last item in input iterable is just a path seperator:
                # > treat as a directory indicator, not an absolute path, and skip
                # > ( unless it's the only path_part, is which case set absolute )
                if path_part in self.input_seps:
                    is_dir = True
                    if len(_iterable) <= 1:
                        is_abs = True
                        break
                    continue # (NOTE: skipping is vital to avoid is_abs check in this case)

                # otherwise, check if path_parts ends with trailing slash
                elif path_part.endswith(self.input_seps):
                    is_dir = True

            # check if current part is absolute
            if path_part.startswith(self.input_seps):
                is_abs = True

            # add individual path part segments to parts
            # i.e. PathPart '/path/to/file.txt' -> Segments '(path, to, file.txt)'
            parts.extend(segment for segment in reversed(re.split(split_pattern, path_part)) if segment)

            # if path is absolute, we take it as the start of the URI and discard the rest
            if is_abs:
                break

        return tuple(reversed(parts)), is_abs, is_dir

        

            

        