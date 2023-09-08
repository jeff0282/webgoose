

from    typing      import     List
from    typing      import     Optional
from    typing      import     Tuple
from    typing      import     Type



class BaseNode:

    """
    Base Trie Tree Node for Webgoose Pre-Build 
    Directory Tree Representation

    Not for direct use, cannot take children
    """

    EXT_DELIMITER = "."


    def __init__(self,
                 name: str,
                 parent: Type["BaseNode"] = None) -> None:

        """
        Create a Base Trie Tree Node

        Not for direct use, use appropriate subclass
        """

        # Set private variables (for clarity)
        self._name: str = ""
        self._parent: Optional[Type["BaseNode"]] = None


        # Set object attributes using designated property setters
        self.name = name
        self.parent = parent


    def __bool__(self) -> bool:
        """ Sanity Check """
        return True


    def __repr__(self) -> str:
        """ Return in form ClassName('Node Name') """
        return f"{self.__class__.__name__}('{self.name}')"
    

    def __str__(self) -> str:
        """ Return in form ClassName('Node Name') """
        return self.__repr__()
    

    def __lt__(self, cmp: Type["BaseNode"]) -> bool:
        """
        Implement Less-Than using Unicode Order (case insensitive)
        """
        return self.name.casefold() < cmp.name.casefold()


    def __gt__(self, cmp: Type["BaseNode"]) -> bool:
        """
        Implement Greater-Than using Unicode Order (case insensitive)
        """
        return self.name.casefold() > cmp.name.casefold()
    

    def __del__(self) -> None:
        """
        Ensure proper unlinking on deletion
        """
        self.unlink()


    @property
    def name(self) -> str:
        """
        The full name of the node
        """
        return self._name
    

    @name.setter
    def name(self, new_name: str) -> None:
        """
        Change the name of this node
        """

        # keep old name back just incase
        old_name = self._name
        self._name = new_name

        # if this node has a parent, check that it's still a valid child
        if self.parent:
            if not self.parent._check_child_suitability(self):
                self._name = old_name
                raise ValueError(f"New name '{new_name}' is not valid for children of parent node '{self.parent}'")
    

    @property
    def parent(self) -> Optional[Type["BaseNode"]]:
        """
        The parent of this node

        If node has no parent, returns None
        """

        return self._parent


    @parent.setter
    def parent(self, new_parent: Optional[Type["BaseNode"]]) -> None:
        """
        Set the parent of this node

        If new parent is None, simply detaches the node

        Throws ValueError if new parent can't take children
        """

        # If new parent is truthy, attempt to attach this node to it as a child
        if new_parent:
            try:
                new_parent._attach_child(self)

            except AttributeError as e:
                raise ValueError(f"The provided parent node '{new_parent}' cannot take children") from e
            

        # If old parent is truthy, attempt to detach this node from it
        # (if exception raised here, then something is very fucked) <- THE technical explanation
        # (if node has been attached, it should also be possible to detach unless there's an implementation issue somewhere)
        if self._parent:
            self._parent._detach_child(self)

        # if nothing has exploded, set new parent
        self._parent = new_parent


    @property
    def base(self) -> str:
        """
        The basename of the node

        Ignores leading seperator for hidden files

        e.g.    file.txt                -> file
                .hidden_file.txt        -> .hidden_file
                file.tar.gz             -> file
        """
        
        name_parts = self._name.split(self.EXT_DELIMITER)
        
        if not name_parts[0]:
            return name_parts[1]
        
        return name_parts[0]
    

    @property
    def exts(self) -> Tuple[str, ...]:
        """
        The extension(s) as a tuple of strings, with separators removed

        Ignores leading seperator for hidden files

        e.g.    file.txt                -> ["txt"]
                .hidden_file.txt        -> ["txt"]
                file.tar.gz             -> ["tar", "gz"]
        """

        name_parts = self._name.split(self.EXT_DELIMITER)

        if not name_parts[0]:
            return name_parts[2:]
        
        return name_parts[1:]

    
    @property
    def ext(self) -> str:
        """
        The extension(s) as a string

        Ignores leading seperator for hidden files

        e.g.    file.txt                -> .txt
                .hidden_file.txt        -> .txt
                file.tar.gz             -> .tar.gz
        """

        return self.EXT_DELIMITER.join(self.exts())
    

    def unlink(self) -> None:
        """
        Unlink this node from it's parent

        (Equivalent to setting node.parent = None)
        """

        # use property setter to do heavt lifting
        self.parent = None