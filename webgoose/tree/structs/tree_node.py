
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

    PATH_DELIMITER = "/"

    def __init__(self,
                name:       Union[Tuple[str, str], str],
                parent:     Optional[Type['TreeNode']]  = None,
                metadata:   Dict[str, Any]              = dict()) -> None:
        """
        Create a site tree TreeNode object.

        Takes a unix-valid filename and (optionally) a parent node and metadata.
        The metadata dict is proxied out as keys of an instance.

        This class CANNOT (really) and SHOULD NOT be used directly, instead use via subclasses.
        """

        # Set some initial default values
        # (some of the property setters expect the attrs to exist)
        self._name_stack: List[Tuple[str]] = []
        self._parent: Optional[Type['TreeNode']] = None

        # Set provided params
        self.name = name
        self.parent = parent
        self.metadata = metadata


    #
    # Dunder Methods
    # ---

    def __getitem__(self, key: str) -> Any:
        """ Allow proxying of metadata to keys of an instance """

        return self.metadata[key]

    
    def __setitem__(self, key: str, value: Any) -> None:
        """ Allow proxied metadata keys to be set """

        self.metadata[key] = value


    def __delitem__(self, key: str) -> None:
        """ Allow deletion of proxied metadata keys """

        self.metadata[key].pop()


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
        """
        The current name of a node

        May differ from that set at instantiation if this node
        as been mounted to another tree
        """
        return "".join(self._name_stack[-1])
        


    @name.setter
    def name(self, new_name: Union[Tuple[str, str], str]) -> None:
        """
        Set a new name for a node.

        Throws a ValueError if the name is invalid
        """
        
        # split name into basename and extension
        # if string, use splitext() to create (basename, ext) tuple
        base, ext = new_name if type(new_name) == tuple else os.path.splitext(new_name)

        # check if name is valid
        if not self._name_is_valid(base + ext):
            raise ValueError(f"The name '{new_name}' is invalid for node type '{self.__class__.__name__}'")
        
        # If name stack if empty, simply add it
        # otherwise, replace the last item in the list with the new name
        if self._name_stack:
            self._name_stack[-1] = (base, ext)
        
        else:
            self._name_stack.append((base, ext))


    
    @property
    def ext(self) -> str:
        """
        Get the extension from the node name
        """

        return self._name_stack[-1][1]


    
    @ext.setter
    def ext(self, new_ext: str) -> None:
        """
        Change the extension of the node's name

        File extension can be removed by setting it to the empty string
        """

        # If string isn't empty, check if the first char is a dot
        # if not, the extension isn't valid
        if new_ext:
            if new_ext[0] != ".":
                raise ValueError(f"Invalid Extension '{new_ext}', did you mean '.{new_ext}'?")

        # Name property setter checks full name
        # if new_ext is "", name will just be basename
        self.name = (self.basename, new_ext)


    @property
    def basename(self) -> str:
        """
        Get the basename from the node name
        """

        return self._name_stack[-1][0]
    

    @basename.setter
    def basename(self, new_basename: str) -> None:
        """
        Change the base of the node's name
        """

        # Name property setter checks full name
        self.name = (new_basename, self.ext)



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
