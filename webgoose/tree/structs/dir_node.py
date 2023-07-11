
import  fnmatch

from    typing      import      Any
from    typing      import      Dict
from    typing      import      Callable
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



    def get(self, path: str) -> Type[TreeNode]:
        """ 
        Get child node by path 
        
        Throws NodeNotFoundError if path doesn't exist
        """

        def traversal_func(starting_node:   TreeNode, 
                           path_parts:      Tuple[str, ...]) -> Tuple[TreeNode]:
            
            """
            Simple matching function for use with ``_traverse_to_path()``
            Matches a single file, no wildcards.
            """

            current_node = starting_node
            for name in path_parts:

                # there should only be one match here (unless duplicate checking broken :/)
                match = tuple(filter(lambda node: node.name == name, current_node.children))

                # if no match found, raise exception as path does not exist
                if not match:
                    raise NodeNotFoundError(f"The path '{path}' does not exist")

                current_node = match[0]

            # Return found node in a tuple
            # (_traverse_to_path() typing expects this)
            return (current_node,)

        # Use helper func above to get node with provided name
        matches = self._traverse_to_path(path, traversal_func)

        # if no exceptions raised, matches should have len == 1
        return matches[0]



    def glob(self, pattern: str) -> Tuple[TreeNode]:
        """
        Implements glob for site tree
        """

        def glob_traversal(starting_node:   TreeNode,
                           path_parts:      Tuple[str, ...]) -> Tuple[TreeNode, ...]:
            
            """
            le globby :)
            """

            # Get glob matches for first name in path parts
            matches = []
            for child in starting_node.children:
                matches.append(child) if fnmatch.fnmatch(child.name, path_parts[0]) else None

            # if not at end of path parts:
            # > glob dirs with path_parts[1:]
            # > remove non-directories from matches
            if path_parts[1:]:
                glob_dir = lambda match: glob_traversal(match, path_parts[1:])
                matches = [glob_dir(match) for match in matches if isinstance(match, Directory)]

            return matches

        # Use globing helper func with traverse_to_path
        return self._traverse_to_path(pattern, glob_traversal)

    
    

    def has(self, name_pattern: str) -> bool:
        """ 
        Check if this node has a child node with name matching glob expression 
        """

        child_names = [child.name for child in self.children]
        return any(fnmatch.filter(child_names, name_pattern))

    

    #
    # Private API
    # ---

    def _traverse_to_path(self, 
                          path: str, 
                          traversal_func: Callable[[TreeNode, Tuple[str]], Tuple[TreeNode, ...]]) -> Tuple[TreeNode, ...]:
        """ 
        Traverse a path and return found node, supports relative and absolute paths 
        
        Thrown NodeNotFoundError if path does not exist
        """

        # clean trailing slash if necessary
        if path.endswith(self.PATH_DELIMITER):
            path = path[:-len(self.PATH_DELIMITER)]

        # split path into its pieces
        path_parts = path.split(self.PATH_DELIMITER)

        # If path is absolute, set starting point to root, else use current node
        starting_node = self
        if path_parts[0] == "":
            path_parts.pop(0)
            starting_node = self.root

        # Use given function to traverse to a path
        # providing the setup shit above :3
        return traversal_func(starting_node, path_parts)






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




        