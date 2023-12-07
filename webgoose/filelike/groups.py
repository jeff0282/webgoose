
from    typing      import      Any
from    typing      import      Iterable
from    typing      import      Type

from    collections     import      deque
from    dataclasses     import      dataclass
from    dataclasses     import      field
from    wcmatch         import      glob

from    .               import      FileLike
from    .               import      NotIndexableError
from    .               import      URI



class FileList:
    """
    A List-Like iterable with helpful methods for searching and grouping files
    """

    @dataclass()
    class DirNode:
        """
        A little dataclass acting as an internal tree-node for file lists

        An internal component of FileLists
        """

        name:       str
        files:      list[Type[FileLike]]            = field(default_factory=lambda: [])
        subdirs:    list[Type['FileList.DirNode']]  = field(default_factory=lambda: [])
        index:      Type[FileLike] | None           = None


        def __contains__(self, cmp: str) -> bool:
            """
            Check if this node has a child with name
            """

            return cmp in self.files or cmp in self.subdirs
        

        def get_file(self, name: str, _default: Any = None) -> Type[FileLike] | Any:
            """
            Get a file from this Directory Node by it's string name
            """

            for file in self.files:
                if file.filename == name:
                    return file
                
            # if file not found, return default
            return _default


        def get_dir(self, name: str, _default: Any = None) -> Type['FileList.DirNode'] | Any:
            """
            Get a subdirectory from this Directory Node by it's string name
            """

            for subdir in self.subdirs:
                if subdir.name == name:
                    return subdir
                
            # if no subdirs found with name, return default
            return _default


    # ---
    # Class Attrs
    GLOB_REC_STR   = "**"


    # ---
    # Instance Attr Typing
    _tree: Type[DirNode]


    def __init__(self) -> None:
        """
        Create an empty FileGroup instance
        """
        
        self._tree = self.DirNode("")


    def __bool__(self) -> bool:
        """
        Truthiness is determined by whether the root tree node is truthy
        """

        return bool(self._tree)
    

    def __contains__(self, cmp: Type['URI'] | Type[FileLike] | str) -> bool:
        """
        Perform contain checks with either URI instances, FileLike instances, or strings

        - URI/string instances: Searches for the file using FileList.get(), returns True if no error raised
        - FileLike instances: Extracts slug and does same as above, if file with same slug found checks if
          it's the same object as the one provided
        """

        # boolean for whether we're matching a FileLike object ref
        instance_match = False

        # get URI instance from provided data
        if isinstance(cmp, FileLike):
            cmp = cmp.slug
            instance_match = True

        #
        # Try to get file, perform object match if necessary.
        try:
            file = self.get(cmp)
            if instance_match:
                return file is cmp
            return bool(file)
        
        except TypeError:
            # either a malformed comparison string, or incorrect comparison type
            return False

        except FileNotFoundError:
            # this filelist doesn't have the file specified
            return False
        

    def add(self, file_to_add: Type[FileLike], as_index: bool = False) -> None:
        """
        Add a File to this File List

        Raises:
        - FileExistsError: if path given is already in-use or conflicts with another file
        - NotIndexableError: if as_index is True and the given file is not indexable
        """

        if file_to_add.slug in self:
            raise FileExistsError(f"Cannot Add File: '{file_to_add.slug}' already exists")

        # attempt to create path for file
        dir = self._make_path(file_to_add.slug.dirname)

        # if adding as an index, check:
        # - if the file can be indexed
        # - if directory already has an index
        if as_index:
            if not file_to_add.is_indexable():
                raise NotIndexableError(f"Cannot Add Directory Index: File '{file_to_add}' does not support being used as a Directory Index")
            
            if dir.index:
                raise FileExistsError(f"Cannot Add Directory Index: Directory Index already registered for '{file_to_add.slug.dirname}'")
            
            # if no errors raised, we can set the index
            dir.index = file_to_add

        # finally, add this file to the dir's files
        dir.files.append(file_to_add)
        

    def get(self, path: str | Type[URI]) -> Type[FileLike]:
        """
        Get a item from this FileList with a given Path (string or URI instance)

        Paths are searched relative to the root; absolute path searches will turn up empty

        Raises:
        - FileNotFoundError: if path given doesn't exist in this File List
        """

        # convert path to URI instance if not already
        if isinstance(path, str):
            path = URI(path)

        search_path: Type[URI] = path
        current_dir: Type[FileList.DirNode] = self._tree
        while current_dir:

            # if we haven't matched anything on search path is empty
            # try to get an index of the current_dir
            if len(search_path) == 0:
                if current_dir.index:
                    return current_dir.index
                
                # if no match, break as this is the last check
                break

            # if we're on the last path part, try to get a file
            # if none match, we'll check for index in next iter
            elif len(search_path) == 1:
                file = current_dir.get_file(search_path[0], None)
                if file:
                    return file
            
            # set next dir and trim search path for next iter
            current_dir = current_dir.get_dir(search_path[0], None)
            search_path = search_path[1:]


        # if we reach here, part of the search URI hasn't matched
        raise FileNotFoundError(f"The file '{path}' is not present in this FileList")


    def glob(self, glob_exp: str) -> Type['FileList']:
        """
        Create a subset of this FileList using a Glob Expression
        """

        # if glob expression ends with slash, look only for directory indexes
        index_only = glob_exp.endswith(URI.path_sep)

        # convert glob expression to URI instance
        glob_exp = URI(glob_exp)
        fl = self.__class__()
        for item in self._glob(glob_exp, [self._tree], index_only=index_only):
            fl.add(item)

        return fl

    
    def _glob(self, 
              glob_exp: Type[URI], 
              part_matches: Iterable[Type[DirNode]],
              *,
              index_only: bool = False
              ) -> list[Type[DirNode] | Type[FileLike]]:
        """
        Internal method for self.glob

        Dispatches glob expression operations on dirs provided depending
        on first item on glob expression
        """

        while glob_exp:
            if glob_exp[0] == self.GLOB_REC_STR:
                return self._rglob(glob_exp[1:], part_matches, index_only=index_only)
        
            part_matches = self._stdglob(glob_exp, part_matches, index_only=index_only)
            glob_exp = glob_exp[1:]
        
        return part_matches

    
    def _rglob(self, 
               glob_exp: Type[URI], 
               part_matches: Iterable[Type[DirNode]],
               *,
               index_only: bool = False
               ) -> list[Type[DirNode] | Type[FileLike]]:
        """
        Apply _glob_dispatch to every dir provided recursively
        """

        matches = []
        queue = deque(part_matches)
        while queue:
            curdir = queue.pop()
            queue.extendleft(curdir.subdirs)
            matches.extend(self._glob(glob_exp, [curdir], index_only=index_only))

        return matches


    def _stdglob(self, 
                 glob_exp: Type[URI], 
                 part_matches: Iterable[Type[DirNode]],
                 *,
                 index_only: bool = False
                 ) -> list[Type[DirNode] | Type[FileLike]]:
        """
        Match the files and subdirs by name using a glob expression

        Only handles single directories, does not touch their subdirs
        """

        matches = []

        # if glob expression is empty, so should the results
        if len(glob_exp) < 1:
            return matches
        
        # if we're on the last part of the glob expression, look for only files or indexes
        elif len(glob_exp) == 1:
            # if looking for indexes, get the index of every subdir of dirs provided
            # the subdir's name matches glob expression (and the index exists, ofcourse)
            if index_only:
                for dir in part_matches:
                    matches.extend(subdir.index for subdir in dir.subdirs if glob.globmatch(subdir.name, glob_exp[0]))

            # otherwise, grab every file from dirs provided if it matches the glob expression
            else:
                for dir in part_matches:
                    matches.extend(file for file in dir.files if glob.globmatch(file.filename, glob_exp[0]))
        
        # otherwise, we're matching subdirs
        # return every subdir that matches the current glob expression part
        else:
            for dir in part_matches:
                matches.extend(subdir for subdir in dir.subdirs if glob.globmatch(subdir.name, glob_exp[0]))

        return matches



    def _make_path(self, path: Type[URI]) -> Type[DirNode]:
        """
        Ensure that the path provided in slug exists

        Raises:
        - FileExistsError: if any of the parts of the directory path conflict with an existing filename
        """

        # create and store directory nodes to be made
        # so we can pre-emptively find conflicts
        path_built:     list[str]   = []
        dirs_to_build:  list[tuple[Type[FileList.DirNode], Type[FileList.DirNode]]] = []
        current_dir:    Type[FileList.DirNode] = self._tree
        while current_dir and path:

            # if current path part conflicts with a filename in current directory, cannot proceed
            if current_dir.get_file(path[0], None):
                raise FileExistsError(f"Cannot Construct Path: Path interferes with existing file list entry '{str(URI(*path_built, path[0]))}'")
            
            # if no conflict, if current directory has a subdir with current path part, use it, otherwise create one
            new_dir = current_dir.get_dir(path[0], None)
            if not new_dir:
                new_dir = FileList.DirNode(path[0])
                dirs_to_build.append((current_dir, new_dir))
            
            # update path_built and current_dir, trim path, and proceed to next iter
            current_dir = new_dir
            path_built.append(path[0])
            path = path[1:]

        # if no errors, we can build the path from what we've found
        for par_dir, new_dir in dirs_to_build:
            par_dir.subdirs.append(new_dir)

        # current node will be equal to last node built
        return current_dir