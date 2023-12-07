
from    typing      import      Any
from    typing      import      Iterable
from    typing      import      Type

from    collections     import      deque
from    dataclasses     import      dataclass
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
        files:      list[Type[FileLike]]            = []
        subdirs:    list[Type['FileList.DirNode']]  = []
        index:      Type[FileLike] | None           = None


        def __contains__(self, cmp: str) -> bool:
            """
            Check if this node has a child with name
            """

            return cmp in self.files or cmp in self.subdirs
    

        def __bool__(self) -> bool:
            """
            A DirNode should be truthy if it has children
            """
            return bool(self.files) and bool(self.subdirs)
        

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
            search_path = cmp.slug
            instance_match = True

        #
        # Try to get file, perform object match if necessary.
        try:
            file = self.get(search_path)
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

            # try to get next dir
            # if we're on the last path part, either file or dir index
            next_dir = current_dir.get_dir(search_path[0], None)
            if len(search_path) == 1:
                
                # if we matched a dir on the last path part, attempt to get index
                if next_dir:
                    if next_dir.index:
                        return next_dir.index    

                # if dir wasn't matched, attempt to get a file
                else:
                    file = current_dir.get_file(search_path[0])
                    if file:
                        return file
                    
            # trim search path, and set current dir
            search_path = search_path[1:]

            # if next_dir == None here, the path doesn't exist
            current_dir = next_dir


        # if we reach here, part of the search URI hasn't matched
        raise FileNotFoundError(f"The file '{path}' is not present in this FileList")


    def glob(self, glob_exp: str) -> Type['FileList']:
        """
        Create a subset of this FileList using a Glob Expression
        """

        index_only = glob_exp.endswith(URI.path_sep)
        glob_exp = URI(glob_exp)

        dirs = [self._tree]
        matches = FileList()
        while glob_exp:
            dirs, files = self._glob_dispatch(glob_exp, dirs, index_only=index_only)
            glob_exp = glob_exp[1:]
            matches.add(files)

        return matches

    
    def _glob_dispatch(self, 
                       glob_exp: Type[URI], 
                       dirs: Iterable[Type[DirNode]],
                       *,
                       index_only: bool = False
                       ) -> tuple[list[Type[DirNode]], list[Type[FileLike]]]:
        """
        Dispatches glob expression operations on dirs provided depending
        on first item on glob expression
        """

        if glob_exp[0] == self.GLOB_REC_STR:
            dirs, files = self._rglob(glob_exp[1:], dirs, index_only=index_only)
        
        else:
            dirs, files = self._stdglob(glob_exp, dirs, index_only=index_only)

        return dirs, files
    

    def _rglob(self, 
               glob_exp: Type[URI], 
               dirs: Iterable[Type[DirNode]],
               *,
               index_only: bool = False
               ) -> tuple[list[Type[DirNode]], list[Type[FileLike]]]:
        """
        Apply _glob_dispatch to every dir provided recursively
        """

        dirs = []
        files = []
        queue = deque(dirs)
        while queue:
            curdir = queue.pop()
            queue.extendleft(curdir.subdirs)
            new_dirs, new_files = self._glob_dispatch(glob_exp, [curdir], index_only=index_only)
            dirs.extend(new_dirs)
            files.extend(new_files)

        return dirs, files


    def _stdglob(self, 
                 glob_exp: Type[URI], 
                 dirs: Iterable[Type[DirNode]],
                 *,
                 index_only: bool = False
                 ) -> tuple[list[Type[DirNode]], list[Type[FileLike]]]:
        """
        Match the files and subdirs by name using a glob expression
        """

        dirs = []
        files = []
        # if glob expression is empty, so should the results
        if len(glob_exp) < 1:
            return dirs, files
        
        # if we're on the last part of the glob expression, look for only files or indexes
        if len(glob_exp) == 1:
            # if looking for indexes, get the index of every subdir of dirs provided
            # the subdir's name matches glob expression (and the index exists, ofcourse)
            if index_only:
                for dir in dirs:
                    files.extend(subdir.index for subdir in dir.subdirs if glob.globmatch(subdir.name, glob_exp[0]))

            # otherwise, grab every file from dirs provided if it matches the glob expression
            else:
                for dir in dirs:
                    files.extend(file for file in dir.files if glob.globmatch(file.filename, glob_exp[0]))
        
        # otherwise, we're matching subdirs
        else:
            for dir in dirs:
                dirs.extend(subdir for subdir in dir.subdirs if glob.globmatch(subdir.name, glob_exp[0]))

        # return what we've found
        return dirs, files



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
        while path:

            # if current path part conflicts with a filename in current directory, cannot proceed
            if current_dir.get_file(path[0], None):
                raise FileExistsError(f"Cannot Construct Path: Path interferes with existing file list entry '{str(URI(*path_built, path[0]))}'")
            
            # if no conflict, if current directory has a subdir with current path part, use it, otherwise create one
            new_dir = current_dir.get_dir(path[0], None)
            if not dir:
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