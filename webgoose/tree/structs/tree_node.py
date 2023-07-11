
import  os

from    typing      import      Any
from    typing      import      Dict
from    typing      import      Generator
from    typing      import      List
from    typing      import      Optional
from    typing      import      Tuple
from    typing      import      Type
from    typing      import      Union


class TreeNode:
    """
    Base node implementation for site tree nodes. Not For Direct Use.

    Implements a singly linked, file system like tree.
    """

    PATH_DELIMITER = os.sep
    EXT_DELIMITER  = os.extsep


    def __init__(self,
                name:       Union[Tuple[str, ...], str],
                parent:     Optional[Type['TreeNode']]  = None,
                metadata:   Dict[str, Any]              = dict()) -> None:
        """
        Create a site tree TreeNode object.

        Takes a unix-valid filename and (optionally) a parent node and metadata.
        The metadata dict is proxied out as keys of an instance.

        This class CANNOT (really) and SHOULD NOT be used directly, instead use via subclasses.
        """

        # Set 'private' instance vars to default values
        self._name_stack: List[Tuple[str]] = []
        self._parent: Optional[Type['TreeNode']] = None

        # Set provided params
        self.name = name
        self.parent = parent
        self.metadata = metadata


    #
    # Dunder Methods
    # ---


    def __del__(self) -> None:
        """ Ensure references of this instance in parent nodes are clearer before deletion """

        if self.parent:
            self.unlink(quiet=True)


    def __str__(self) -> str:
        """ Return string version of TreeNodes as ClassName(<path>) """

        return f"{self.__class__.__name__}('{self.path}')"
    

    def __repr__(self) -> str:
        """ Make instance string human readable """

        return self.__str__()
    

    def __bool__(self) -> bool:
        """ TreeNode objects should NEVER be falsey """
        
        return True
    


    #
    # Public API
    # ---


    @property
    def name(self) -> str:
        """ Return the full name of this node """

        return self._name_stack[-1]
    


    @name.setter
    def name(self, new_name: Union[Tuple[str, ...], str]) -> None:
        """ Change name of this node """

        # Check if name is valid
        if not self._name_is_valid(new_name):
            raise ValueError(f"The name '{new_name}' is not valid for node '{self.__class__.__name__}'")

        # If node has a parent, check for potential name conflict
        if self.parent:
            if self.parent.has(new_name):
                raise ValueError(f"The parent node '{self.parent}' already has a child with name '{new_name}'")

        # If no exception raised, change the name
        # (name stack may be empty, so we check that the length is truthy before popping)
        self._name_stack.pop() if len(self._name_stack) else None
        self._name_stack.append(new_name)



    @property
    def basename(self) -> str:
        """ 
        Return the basename of this node; the filename without extensions
        
        For example: 
            - index.html        > index
            - .hidden_file.txt  > .hidden_file
        """

        return self._split_name(self.name)[0]



    @property
    def exts(self) -> Tuple[str]:
        """
        Return the file extensions as a tuple of strings

        For example: "file.tar.gz" -> ["tar", "gz"]
        """

        return self._split_name(self.name)[1]



    @property
    def ext(self) -> str:
        """
        Return the file extensions as a string joined by the
        extension delimiter

        For example: "file.tar.gz" -> ".tar.gz"
        """

        exts = self._split_name(self.name)[1]
        return self.EXT_DELIMITER + self.EXT_DELIMITER.join(exts)



    @property
    def parent(self) -> Optional[Type['TreeNode']]:
        """ Return the parent node of this node """

        return self._parent
    


    @parent.setter
    def parent(self, new_parent: Optional[Type['TreeNode']]) -> None:
        """
        Set a new parent for this node.

        Just attempts to ask the new parent to add this instance to it.
        """
        
        # If the new_parent is None, just unlink
        if not new_parent:
            return self.unlink(True)
        
        # Otherwise, attempt to add this node to the new_parent
        try:
            new_parent.add(self)

        # If an exception is raised here, the node should be unaffected
        except AttributeError as e:
            raise ValueError(f"Node '{new_parent}' cannot take children") from e



    @property
    def parts(self):
        """
        Get the 'parts' of the path from this node to root.

        Returns in the form (root, ... , this node)
        """

        parts = [self]
        for node in self._gen_traverse_up():
            parts = [node, *parts]
        
        return parts



    @property
    def path(self) -> str:
        """ Return full path from root to this node """

        return self.PATH_DELIMITER.join(part.name for part in self.parts)



    def rel_parts(self, relative_to: Type['TreeNode']) -> Tuple[Type['TreeNode']]:
        """ Same as .parts but relative to any node between this node and root """

        parts = [self]
        for node in self._gen_traverse_up():
            parts = [node, *parts]

            if node is relative_to:
                return parts

        # If not yet returned, node wasn't found
        raise ValueError(f"Node '{relative_to}' does not exist between this node '{self}' and root")



    def rel_path(self, relative_to: Type['TreeNode']) -> str:
        """ Same as .path but relative to any node between this and root"""

        return self.PATH_DELIMITER.join(part.name for part in self.rel_parts(relative_to))    



    def unlink(self, quiet: bool = False) -> None:
        """ Unlinks this node from it's parent """

        # If no parent, just exit
        # raise exception, unless quiet is True
        if not self.parent:
            if quiet:
                return 
            
            raise Exception("Node has no parent")
        

        # Request that the parent remove this node from itself
        self.parent._unlink_node(self)



    #
    # Private API
    # ---

    def _split_name(self, name: str) -> Tuple[str, Tuple[str, ...]]: 
        """ Split a name by basename and extensions """

        # seperate the filename by the extension delimiter
        # (the list created here will always have len > 0)
        fname_parts = self.name.split(self.EXT_DELIMITER)
        

        # if only one name parts, no extensions
        if len(fname_parts) == 1:
            return tuple(fname_parts[0], tuple())

        # Otherwise, length > 1,
        # if first item is "", this must be a hidden file name (".hidden_file")
        # in this case, extensions are the 3rd and subsequent fname parts 
        if fname_parts[0] == "":
            basename = self.EXT_DELIMITER.join(fname_parts[:2])
            return (basename, tuple(fname_parts[2:]))
        
        # If not hidden file, first name_part must be the basename
        # exrs are 2nd and subsequent fname parts
        return (fname_parts[0], tuple(fname_parts[1:]))



    def _name_is_valid(self, name: str) -> bool:
        """ Check if a name is valid for this type of node """

        # TODO !!
        return bool(name)


    def _gen_traverse_up(self) -> Generator['TreeNode', None, None]:
        """ 
        Generator that traverses up a tree to root 
        
        First item is the PARENT of a node, NOT the node itself
        """

        current_node = self.parent

        while(current_node):
            yield current_node
            current_node = current_node.parent
