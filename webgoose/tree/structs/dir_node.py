
from    typing      import      Any
from    typing      import      Dict
from    typing      import      Iterator
from    typing      import      List
from    typing      import      Optional
from    typing      import      Tuple
from    typing      import      Type
from    typing      import      Union

from    webgoose.tree.structs   import  DuplicateChildNameError
from    webgoose.tree.structs   import  NodeNotFoundError
from    webgoose.tree.structs   import  TreeNode




class Directory(TreeNode):


    # Class Constants
    ROOT_DIR_NAME = ""

    def __init__(self,
                 name:      str,
                 parent:    Optional[Type[TreeNode]]    = None,
                 metadata:  Dict[str, Any]              = dict(),
                 children:  Tuple[Type[TreeNode]]       = tuple()) -> None:
        """
        Create a Directory Node
        """

        # Initialise private vars with default values
         # (second item in name stack left blank as placeholder for actual name)
        self._name_stack = [self.ROOT_DIR_NAME, ""]

        # Create The Base TreeNode
        super().__init__(name, parent, metadata)

        # Add Children
        self._children: List[TreeNode] = []
        for child in children:
            self.add(child)


    
    #
    # Dunder Methods
    # ---

    def __iter__(self) -> Iterator[Type[TreeNode]]:
        """ Make Directories Iterable, using their tuple of children """

        return iter(self._children)
    

    def __len__(self) -> int:
        """ Get length of directory's tuple of children"""

        return len(self._children)


    def __contains__(self, object: Any) -> bool:
        """ Check if this node has a certain child node """

        return (object in self.__children)



    #
    # Public API
    # ---


    @TreeNode.name.getter
    def name(self) -> str:
        """ 
        Return the name of this node 
        
        If this node is a root node, this will return the 
        default root node name, regardless of what is otherwise set

        The decorator is an unfortunate consequence of shitty python property
        inheritance. Overidding a single property getter/setter/deleter without
        overiding them all results in them being detached. Without explicitly declaring we
        want to override the TreeNode.name property, the Directory.name property will be detached
        from the TreeNode.name.setter, instead of being implicity inherited :(
        """

        # Overrides default implementation in order to work with name stack
        if self.is_root:
            return self._name_stack[0]
        
        return self._name_stack[-1]


    @property
    def is_root(self) -> bool:
        """ Check if this node is the root directory in its respective tree """

        # Simply return False if node's parent is set
        return not bool(self.parent)



    @property
    def children(self) -> Tuple[Type[TreeNode]]:
        """ Get this node's children """

        return tuple(self._children)
    


    @property
    def dirs(self):
        """ Get all children that are an instance of Directory """

        return tuple(child for child in self._children if isinstance(child, Directory))
    


    @property
    def files(self):
        """ Get all children that are not a Directory """

        return tuple(child for child in self._children if not isinstance(child, Directory))

    

    def add(self, *nodes_to_add: Tuple[Type[TreeNode]]) -> None:
        """ 
        Add N number of nodes as children of this node 
        
        Throws DuplicateChildNameError in the event of a name conflict
        betwewwn a current and new child
        """

        for node in nodes_to_add:
            self._add_node(node)



    def get(self, node_strname: str, quiet: bool = False) -> Type[TreeNode]:
        """ Get child node by name """

        # there should only be 0 or 1 matches
        match = [child for child in self._children if child.name == node_strname]

        # if no matches, throw exception or return None depending on 
        # quiet bool is set
        if not match:
            if quiet:
                return None
            
            raise NodeNotFoundError(f"Node with name: '{node_strname}' not found in this ")
        
        # if match found, return it
        return match[0]
    
    

    def has(self, node_strname: str) -> bool:
        """ Check if this node has a child node with a certain name """

        return bool(self.get(node_strname, True))

    

    #
    # Private API
    # ---

    def _add_node(self, node: Type[TreeNode]) -> None:
        """ 
        Add a single node as a child of this node 
        
        Checks for duplicate names, throws DuplicateChildNameError if found
        """

        # check if node with name already exists
        if self.has(node.name):
            raise DuplicateChildNameError(f"Node with name '{node.name}' already exists as a child of node '{self}'")

        # At this point, the parent change should be ok!
        # > cleanly remove new child from old parent, if applicable
        node.unlink(quiet=True)
        # > set new child's parent to this node
        node._parent = self
        # > add new child to this nodes children
        self._children.append(node)


    
    def _unlink_node(self, node: Type['TreeNode']) -> None:
        """ 
        Remove a single node as a child of this node 
        """

        self._children = [child for child in self._children if child is not node]
        node._parent = None


    
    def _change_name(self, new_name: str) -> None:
        """
        Overrides the default implementation to work with
        the name stack
        """

        self._name_stack[-1] = new_name




        