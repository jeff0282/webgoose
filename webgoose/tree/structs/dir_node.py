
from    typing      import      Any
from    typing      import      Dict
from    typing      import      Iterator
from    typing      import      List
from    typing      import      Optional
from    typing      import      Tuple
from    typing      import      Type
from    typing      import      Union

from    webgoose.tree.structs   import  TreeNode



class Directory(TreeNode):


    def __init__(self,
                 name:      Union[Tuple[str, ...], str],
                 parent:    Optional[Type[TreeNode]]    = None,
                 metadata:  Dict[str, Any]              = dict(),
                 children:  Tuple[Type[TreeNode]]       = tuple()) -> None:
        """
        Create a Directory Node
        """

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
        """ Add N number of nodes as children of this node """

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
            
            raise ValueError(f"Node with name: '{node_strname}' not found in this ")
        
        # if match found, return it
        return match[0]
    
    

    def has(self, node_strname: str) -> bool:
        """ Check if this node has a child node with a certain name """

        return bool(self.get(node_strname, True))

    

    #
    # Private API
    # ---

    def _add_node(self, node: Type[TreeNode]) -> None:
        """ Add a single node as a child of this node """


        # check if node with name already exists
        if self.get(node.name, True):
            raise ValueError(f"Node with name '{node.name}' already exists as a child of node '{self}'")

        print("ADDING NODE")
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




        