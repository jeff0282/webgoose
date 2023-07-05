
from    typing      import      Any
from    typing      import      Dict
from    typing      import      Optional
from    typing      import      Type
from    typing      import      Union


class TreeNode:
    """
    Base node implementation for site tree nodes. Not For Direct Use.

    Implements a singly linked, file system like tree.
    """

    def __init__(self,
                name:       str,
                parent:     Optional[Type['TreeNode']]  = None,
                metadata:   Optional[Dict[str, Any]]    = dict()) -> None:
        """
        Create a site tree TreeNode object.

        Takes a unix-valid filename and (optionally) a parent node and metadata.
        The metadata dict is proxied out as keys of an instance.

        This class should NOT be used directly, instead use via a subclass.
        """

        # Set Name and Parent, and Check Validity of Both
        self.set_name(name)
        self.set_parent(parent)

        # Set Other Private Instance Vars
        self.__parent   = parent
        self.__metadata = metadata


    #
    # Dunder Methods
    # ---

    def __getitem__(self, key: str) -> Any:
        """ Allow proxying of metadata to keys of an instance """

        return self.__metadata[key]

    
    def __setitem__(self, key: str, value: Any) -> None:
        """ Allow proxied metadata keys to be set """

        self.__metadata[key] = value


    def __delitem__(self, key: str) -> None:
        """ Allow deletion of proxied metadata keys """

        self.__metadata[key].pop()


    def __del__(self) -> None:
        """ Ensure references of this instance in parent nodes are clearer before deletion """

        if self.parent:
            self.unlink()


    def __str__(self) -> str:
        """ Return string version of TreeNodes as ClassName(<path>) """

        return f"{self.__class__.__name__('{self.path}')}"
    


    #
    # Public API
    # ---

    @property
    def name(self) -> str:
        """
        Returns the Human Readable name of a node.

        May NOT represent the raw name.
        """
        return self.__name
    

    @property
    def raw_name(self) -> str:
        """ Returns the raw, unaltered name of a node """
        return self.__name
        

    @name.setter
    def set_name(self, new_name) -> None:
        """
        Set a new name for a node.

        Throws a ValueError if the name is invalid
        """
        if not self.__name_is_valid(new_name):
            raise ValueError(f"The name '{new_name}' is invalid for node type '{self.__class__.__name__}'")
        
        self.__name = new_name


    @property
    def parent(self) -> Union[Type['TreeNode'], None]:
        """ Return the parent node of this node """

        return self.__parent
    

    @parent.setter
    def set_parent(self, new_parent: Union[Type['TreeNode'], None]) -> None:
        """
        Set a new parent for this node.

        Performs all necessary linking and unlinking from old parent to
        new parent.
        """

        # If parent isn't already set, set it to default value
        if not hasattr(self, "__parent"):
            self.__parent = None
        
        # If new parent is 'None', .unlink() fully and return
        if not new_parent:
            return self.unlink()
        
        # If new parent is a TreeNode, attempt to add this instance to it
        # (if new_parent doesn't have .add(), it cannot take children)
        try:
            new_parent.add(self)
        except AttributeError as e:
            raise ValueError(f"Node '{new_parent}' cannot take children") from e
        
        # If all goes well above, set parent to new parent
        self.__parent = new_parent


    @property
    def parts(self):
        """
        Get the 'parts' of the path from this node to root.

        Returns in the form (root, ... , this node)
        """

        stack = [self]
        current_node = self.parent

        while(current_node):
            stack.push(current_node)
            current_node = current_node.parent

        return tuple(stack)


    @property
    def path(self) -> str:
        """ Return full path from root to this node """

        return self.PATH_DELIMITER.join(part.raw_name for part in self.parts)
    


    def unlink(self) -> None:
        """ Unlinks this node from it's parent """

        if self.parent:
            self.parent.__remove_child(self)

        # set using private parent attr
        # (.set_parent(None) calls this method)
        self.__parent = None



    #
    # Private API
    # ---

    def __name_is_valid(self, name: str) -> bool:
        """ Check if a name is valid for this type of node """

        # TODO !!!!!
        return bool(name)
