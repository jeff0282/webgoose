

from    collections import      deque
from    fnmatch     import      fnmatch

from    typing      import      Any
from    typing      import      Callable
from    typing      import      Dict
from    typing      import      List
from    typing      import      Sequence
from    typing      import      Tuple
from    typing      import      Type

from    webgoose.tree.node     import      BaseNode


class GenericDirectory(BaseNode):
    """
    Generic Directory Tree Node implementation.
    
    Operates similarly to a Trie Node, but with string names rather than 
    single chars.
    """

    # IMPLEMENTATION NOTE:
    #
    # THE PATH DELIMITER AFFECTS THE DETECTION IS ABSOLUTE PATHS
    #
    # ABSOLUTE PATHS ARE DEFINED AS PATHS WHERE, WHEN SPLIT BY THE
    # PATH DELIMITER, THE FIRST ELEMENT'S NAME IS THE EMPTY STRING
    # (in other words, the path starts with the delimiter)
    PATH_DELIMITER = "/"

    # 
    # SPECIAL RULES FOR NAME TRAVERSAL
    #
    SPECIAL_PATH_PARTS = {
            "."     : lambda node: node,
            ".."    : lambda node: node.parent if node.parent else node,
        }


    def __init__(self,
                 name: str,
                 parent: Type[BaseNode] = None,
                 **data: Dict[str, Any]) -> None:
        
        """
        Create a generic directory node.
        """

        super().__init__(name, parent)

        # set default values (required for property setters)
        self._children = []

        self.data = data


    @property
    def children(self) -> Tuple[Type[BaseNode], ...]:
        """
        A sorted list containing all the children of this node
        """

        # basenode implements greater/less-than behaviour
        return sorted(self._children)


    @property
    def subdirs(self) -> Tuple[Type['GenericDirectory'], ...]:
        """
        A sorted list containing all the children of this node that are dirs
        """

        return sorted(node for node in self._children if isinstance(node, GenericDirectory))


    @property
    def files(self) -> Tuple[Type[BaseNode], ...]: 
        """
        A sorted list containing all the children of this node that aren't dirs
        """

        return sorted(node for node in self._children if not isinstance(node, GenericDirectory))
    

    def get(self, path: str) -> Tuple[Type[BaseNode], ...]:
        """
        Get file(s) from a path. Supports glob expressions

        Returns a tuple of matches
        """

        # split path into it's seperate names
        parts = path.split(self.EXT_DELIMITER)

        # determine starting node (relative or absolute path)
        start_node = self
        if parts[0] == "":
            parts.pop(0)
            while(start_node.parent):
                start_node = start_node.parent

        # begin traversal
        stack = deque([start_node])
        matches = []
        while(stack):
            cur_node = stack.pop()
            cur_part, *next_parts = parts

            # if not last part of path, get matching dirs
            if next_parts:

                # perform recursive glob if needed
                if cur_part == "**":
                    matches.extend(self.map(lambda node: node.get(next_parts)))
                    continue


                # if special path part, process and proceed to next iter
                if cur_part in self.SPECIAL_PATH_PARTS:
                    stack.extend(self.SPECIAL_PATH_PARTS[cur_part](cur_node))
                    continue

                # otherwise, add subdirs that match the current path part
                # to the stack, proceed to next iter
                stack.extend(subdir for subdir in cur_node.subdirs if fnmatch(subdir.name, cur_part))
                continue
            

            # if on last part of path, add all matching files to matches and end loop
            matches.extend(file for file in cur_node.files if fnmatch(file.name, cur_part))
            break


        return tuple(matches)


    def map(self, func: Callable[[Type[BaseNode]], None]) -> None: 
        """
        Map a function to this node and all subdirs

        Returns None
        """

        stack = deque([self])
        while stack:
            current_dir = stack.pop()

            # add subdirs to stack before apply func
            # incase func adds subdirs (potential never ending loop)
            stack.append(current_dir.subdirs)
            func(current_dir)


    def _attach_child(self, new_node: Type[BaseNode]) -> None:
        """
        Attach new child to this node

        NOTE: This only creates the parent-to-child link, not the child-to-parent

        Throws ValueError if child node can't be accepted
        """

        # check if child can be accepted, throws an exception if not
        self._check_child_suitability(new_node)

        self._children.append(new_node)


    def _detach_child(self, node_to_rm: Type[BaseNode]) -> None:
        """
        Detach a child node from this node

        NOTE: This only removes the parent-to-child link, not the child-to-parent

        Throws ValueError if node provided isn't a child of this one
        """

        for i, child in enumerate(self._children):
            if child is node_to_rm:
                self._children.pop(i)
                return
                
        # if reached, no match found
        raise ValueError(f"Node '{node_to_rm}' does not exist as a child of '{self}'")
        
        
    def _check_child_suitability(self, new_node) -> None:
        """
        Check if new child node can be accepted as a child

        Throws ValueError if cannot be accepted
        """

        # Allow child is no duplicate name found
        if new_node.name in [child.name for child in self._children]:
            raise ValueError(f"Node {self} doesn't accept child nodes with duplicate names")
        
        # ensure empty directory names are reserved for root directories
        if new_node.name == "":
            raise ValueError(f"Non-root directory cannot have empty directory name")

