
import  os

from    typing      import      Any
from    typing      import      Dict
from    typing      import      Generator
from    typing      import      List
from    typing      import      Optional
from    typing      import      Tuple
from    typing      import      Type
from    typing      import      Union

from    webgoose.tree.structs   import  DuplicateChildNameError
from    webgoose.tree.structs   import  InvalidNameError
from    webgoose.tree.structs   import  InvalidParentError
from    webgoose.tree.structs   import  NodeNotFoundError



class TreeNode:
    """
    Base node implementation for site tree nodes. Not For Direct Use.

    Implements a singly linked, file system like tree.
    """

    # Class Constants
    PATH_DELIMITER = os.sep
    EXT_DELIMITER  = os.extsep


    def __init__(self,
                name:       str,
                parent:     Optional[Type['TreeNode']]  = None,
                metadata:   Dict[str, Any]              = dict()) -> None:
        """
        Create a site tree TreeNode object.

        Takes a unix-valid filename and (optionally) a parent node and metadata.
        The metadata dict is proxied out as keys of an instance.

        This class CANNOT (really) and SHOULD NOT be used directly, instead use via subclasses.
        """

        # Set 'private' instance vars to default values
        self._parent: Optional[Type['TreeNode']] = None

        # Set provided params using provided setters
        # (subclasses may set these differently)
        self.name: str = name
        self.parent: Optional['TreeNode'] = parent
        self.metadata: Dict[str, Any] = metadata


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

        return self._name
    


    @name.setter
    def name(self, new_name: str) -> None:
        """ Change name of this node """

        # Check if name is valid
        if not self._name_is_valid(new_name):
            raise InvalidNameError(f"The name '{new_name}' is not valid for node '{self.__class__.__name__}'")

        # If node has a parent, check for potential name conflict
        if self.parent:

            # keep by some details incase we need to revert
            parent = self.parent
            old_name = self.name

            # unlink from current parent
            self.unlink(quiet=True)

            # change name and attempt to add back to parent
            self._change_name(new_name)
            try:
                parent.add(self)

            # if parent finds a naming conflict, catch exception, restore old name,
            # and raise error afterwards (not dodgy at all :3)
            except DuplicateChildNameError as e:
                self._change_name(old_name)
                parent.add(self)
                raise e

        # if no parent, just change the name
        else:
            self._change_name(new_name)



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
        return self.EXT_DELIMITER + self.EXT_DELIMITER.join(exts) if exts else ""



    @property
    def parent(self) -> Optional[Type['TreeNode']]:
        """ Return the parent node of this node """

        return self._parent
    


    @property
    def is_root(self) -> bool:
        """ 
        Check if this node is the root node 
        
        By default, TreeNodes are NEVER root nodes
        subclasses may change this behaviour
        """

        return False


    @parent.setter
    def parent(self, new_parent: Optional[Type['TreeNode']]) -> None:
        """
        Set a new parent for this node.

        Throws InvalidParentError if the parent provided cannot be used as a parent
        Throws DuplicateChildNameError if naming found conflict in the parent
        """
        
        # If the new_parent is None, just unlink
        if not new_parent:
            return self.unlink(quiet=True)
        
        # Otherwise, attempt to add this node to the new_parent
        try:
            new_parent.add(self)

        # If an exception is raised here, the node should be unaffected
        except AttributeError as e:
            raise InvalidParentError(f"The provided parent node '{new_parent}' cannot take children") from e



    @property
    def parts(self):
        """
        Get the 'parts' of the path from this node to root.

        Returns in the form (root, ... , this node)
        """

        parts = [self]
        for node in self._gen_traverse_up():
            parts = (node, *parts)
        
        return parts



    @property
    def path(self) -> str:
        """ Return full path from root to this node """

        return self._create_path(self.parts)
    


    @property
    def root(self) -> 'TreeNode':
        """
        Get the root node of this tree
        """

        return self.parts[0]



    def rel_parts(self, relative_to: Type['TreeNode']) -> Tuple[Type['TreeNode']]:
        """ Same as .parts but relative to any node between this node and root """

        parts = [self]
        for node in self._gen_traverse_up():
            if node is relative_to:
                return parts
            
            parts = (node, *parts)

        # If not yet returned, node wasn't found
        raise NodeNotFoundError(f"Node '{relative_to}' does not exist between this node '{self}' and root")



    def rel_path(self, relative_to: Type['TreeNode']) -> str:
        """ Same as .path but relative to any node between this and root"""

        return self._create_path(self.rel_parts(relative_to))  



    def unlink(self, quiet: bool = False) -> None:
        """ Unlinks this node from it's parent """

        # If no parent, just exit
        # raise exception, unless quiet is True
        if not self.parent:
            if quiet:
                return 
            
            raise InvalidParentError("This node has no parent to be unlinked from (set quiet=True to avoid this)")
        

        # Request that the parent remove this node from itself
        self.parent._unlink_node(self)



    #
    # Private API
    # --- 


    def _create_path(self, path_parts: Tuple['TreeNode', ...]) -> str:
        """ 
        Create a string path using a tuple of nodes
        """

        if len(path_parts) == 1:
            if path_parts[0].is_root:
                return path_parts[0].name + self.PATH_DELIMITER
            
            return path_parts[0].name

        elif len(path_parts) > 1:
            return self.PATH_DELIMITER.join(part.name for part in path_parts)
        
        # if not yet returned, len(path_parts) < 1 which is invalid
        raise ValueError("Tuple of Nodes must have length > 0")

        


    def _split_name(self, name: str) -> Tuple[str, Tuple[str, ...]]: 
        """ Split a name by basename and extensions """

        # seperate the filename by the extension delimiter
        # (the list created here will always have len > 0)
        fname_parts = name.split(self.EXT_DELIMITER)
        

        # if only one name parts, no extensions
        if len(fname_parts) == 1:
            return (fname_parts[0], tuple())

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


    def _change_name(self, new_name: str) -> None:
        """ 
        Overriddable method to change name, allows for subclasses
        with different ways of storing names to easily change them
        without having to override the default setter
        
        Does NOT check for errors!
        """

        self._name = new_name


    def _gen_traverse_up(self) -> Generator['TreeNode', None, None]:
        """ 
        Generator that traverses up a tree to root 
        
        First item is the PARENT of this node, NOT the node itself
        """

        current_node = self.parent

        while(current_node):
            yield current_node
            current_node = current_node.parent
