
import  fnmatch

from    typing      import      Any
from    typing      import      Dict
from    typing      import      Iterable
from    typing      import      Iterator
from    typing      import      List
from    typing      import      Optional
from    typing      import      Tuple
from    typing      import      Type

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
                 children:  Iterable[Type[TreeNode]]    = tuple()) -> None:
        """
        Create a Directory Node

        TODO: better docstring req'd
        """

        # Initialise private vars with default values
         # (second item in name stack left blank as placeholder for actual name)
        self._name_stack = [self.ROOT_DIR_NAME, None]
        self._children: List[TreeNode] = []

        # Create The Base TreeNode
        super().__init__(name, parent, metadata)

        # Add Children
        self.add(*children)


    
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

    

    def add(self, *nodes: Tuple[Type[TreeNode]]) -> None:
        """ 
        Add N number of nodes as children of this node
        
        Throws DuplicateChildNameError in the event of a name conflict
        betwewwn a current and new child
        """

        for node in nodes:
            self._add_node(node)



    def get(self, path: str) -> Type[TreeNode]:
        """ 
        Get node by path 
        
        Throws NodeNotFoundError if path doesn't exist
        """

        # Split path into it's seperate names
        is_absolute, path_parts = self._split_path(path)

        # if path is absolute, set starting_node to root of this tree
        current_node = self.root if is_absolute else self

        # Iterate through the path parts, attempt to traverse according to path
        for name in path_parts:

            # try to match node by string name
            # there should only be one match here (duplicate names should not be allowed)
            match = tuple(filter(lambda node: node.name == name, current_node.children))

            # if no match found, raise exception as path does not exist
            if not match:
                raise NodeNotFoundError(f"The path '{path}' does not exist")

            # if match found, set it to current node and loop
            current_node = match[0]

        # Return the last found node if out of loop and no exception raised
        return current_node



    def glob(self, pattern: str) -> Tuple[TreeNode]:
        """
        Implements glob for site tree
        """


        def helper_func(starting_node:      Type['TreeNode'],
                        path_parts:         Tuple[str, ...]) -> Tuple[Type[TreeNode], ...]:
            
            """
            Helper function to allow for recursive calls (**) part-way through
            the globbing process :)
            """

            # start globing :3
            partial_matches: List[Type[TreeNode]] = [starting_node]

            # try to match each path part going down the tree
            for name in path_parts:

                # Before looping, filter partial_matches of non-directories
                # non-directories should only be allowed on last iter
                partial_matches = filter(lambda node: isinstance(node, Directory), partial_matches)

                # Recursive glob case
                if name == "**":
                    # TODO: awaiting .map_down() support
                    pass

                # Non-recursive case
                # Check if already matched nodes continue to match the
                # path by checking their children's names, filter out if not
                old_partial_matches = partial_matches
                partial_matches = []
                for node in old_partial_matches:
                    partial_matches.extend(child for child in node.children 
                                           if fnmatch.fnmatch(child.name, name))   
                    
                # if all partial matches have been filtered out, end loop
                if not partial_matches:
                    break;
            
            # Return final partial_matches, convert to tuple    
            return tuple(partial_matches)


        # split path pattern into it's parts
        is_absolute, path_parts = self._split_path(pattern)

        # set starting node
        starting_node = self.root if is_absolute else self

        # Use helper function to glob using above
        return helper_func(starting_node, path_parts)
        


    def has(self, pattern: str) -> bool:
        """ 
        Check if this node has a child node with name matching glob expression 

        This method does NOT support paths, only immediate children
        """

        child_names = [child.name for child in self.children]
        return any(fnmatch.filter(child_names, pattern))

    

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




        