
from    typing      import      Any
from    typing      import      Iterable
from    typing      import      Type

from    dataclasses     import      dataclass

from    .               import      FileLike
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
    # Instance Attr Typing
    _tree: Type[DirNode]


    def __init__(self) -> None:
        """
        Create an empty FileGroup instance
        """
        
        self._tree = self.DirNode()


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
        # If anything other than TypeError or FileNotFoundError are raised,
        # something is very fuckied up :( 
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
        

    def get(self, path: str | Type[URI]) -> Type[FileLike]:
        """
        Get a item from this FileList with a given Path (string or URI instance)

        Paths are searched relative to the root; absolute path searches will turn up empty
        """

        # convert path to URI instance if not already
        if isinstance(path, str):
            path = URI(path)

        search_uri = path
        current_node = self._tree
        while search_uri:

            # if on last part of search URI, search files
            if len(search_uri) == 0:
                file = current_node.get_file(search_uri[0], None)
                if file:
                    return file
                # if no match, break
                break
                
            # otherwise, attempt to match next subdir
            else:
                dir = current_node.get_dir(search_uri[0], None)
                # if match, set current node and trim search_uri for next iteration
                if dir:
                    current_node = dir
                    search_uri = search_uri[1:]
                    continue
                # if no match, break
                break

        # if we reach here, part of the search URI hasn't matched
        raise FileNotFoundError(f"The file '{path}' is not present in this FileList")


    def add(self, file_to_add: Type[FileLike], as_index: bool = False) -> None:
        """
        Add a File to this File List
        """

        # attempt to create path for file
        dir = self._make_path(file_to_add.slug.dirname)

        # if adding as an index, check if index already set for respective dir
        if as_index:
            if dir.index:
                raise FileExistsError(f"Cannot Add Directory Index: Directory Index already registered for '{file_to_add.slug.dirname}'")
            # if index not set for the dir, set this file to be it
            dir.index = file_to_add

        # finally, add this file to the dir's files
        dir.files.append(file_to_add)


    def _make_path(self, path: Type[URI]) -> Type[DirNode]:
        """
        Ensure that the path provided in slug exists

        Raises FileExistsError if any of the parts of the directory path
        conflict with an existing filename
        """

        # construct directory path given
        current_node = self._tree
        while path:

            # if next directory already exists, use it, trim path and skip to next iter
            match_dir = current_node.get_dir(path[0], None)
            if match_dir:
                current_node = match_dir
                path = path[1:]
                continue
            
            # otherwise, create new directory node
            # confirm that making new directory node won't interfere with existing filenames
            match_file = current_node.get_file(path[0], None)
            if match_file:
                raise FileExistsError(f"Cannot Construct Path: Path interferes with existing file list entry '{match_file}'")
            
            # create and add new directory node, set new current node and trim path for next iter
            new_dirnode = FileList.DirNode(path[0])
            current_node.subdirs.append(new_dirnode)
            current_node = new_dirnode
            path = path[1:]

        # if no errors raised, current_node should now be the last directory in the path
        return current_node


