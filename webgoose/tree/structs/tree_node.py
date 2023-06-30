
from    typing      import      Any
from    typing      import      Dict
from    typing      import      Optional
from    typing      import      Tuple


class TreeNode:


    PATH_DELIMITER = "/"

    """
    Basis for nodes of Webgoose site trees

    Implements basic functionality of a tree node ... [tbc]
    """

    def __init__(self, 
                 name: str, 
                 parent: Optional['TreeNode'], 
                 **kwargs: Dict[str, Any]) -> None:

        """
        Base class for Webgoose site tree nodes.

        Takes a name, parent node (optionally), and any user-defined keyword arguments
        Keyword arguments will be available as object attributes, and WILL OVERRIDE attributes if already set
        """

        self.__name: str
        self.__parent: 'TreeNode'

        self.__name = name
        self.__parent = parent
        
        for k, v in kwargs:
            setattr(self, k, v)

    

    @property
    def name(self):
        if self.is_anchor:
            return self.PATH_DELIMITER
        
        return self.__name

    
    @property
    def parent(self):
        return self.__parent
    

    @property
    def uri(self):

        """FUCK THIS I HATE THSIU WTF"""

        parts = self.parts

        if len(parts) <= 1:
            return self.name
        
        # EVILL !!!!!!!
        elif parts[0].is_anchor:
            return self.name + self.PATH_DELIMITER.join([part.name for part in parts[1:]])

        else:
            return self.PATH_DELIMITER.join(parts)

    
    @property
    def is_anchor(self):

        """
        Is this node the anchor node for the tree?

        The default definition of an anchor node is the root node of a site tree.
        However, some nodes may never be anchor nodes, such as files.
        """

        return not bool(self.parent)


    @property
    def parts(self) -> Tuple['TreeNode']:

        """
        Get the 'parts' of the path from this node to root.

        Iteratively traverse to the root of the tree
        Returns a tuple containing the route, in order root > to > start_node
        """

        stack = [self]
        current_node = self.parent

        while(current_node):
            stack.push(current_node)
            current_node = current_node.parent

        return tuple(stack)



