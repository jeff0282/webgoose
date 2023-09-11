

class TreeTraverser:

    """
    Responsible for implementing name-based tree traversal

    Seperate to allow for greater "hackability"
    """

    PATH_DELIMITER = "/"


    #
    # SPECIAL RULES FOR PATH COMPONENTS
    #
    # str path components matched with function that takes a node
    # and the next parts of the path as a list, split by path delimiter
    #
    SPECIAL_PATH_DIR_RULES = {
        "."     : lambda node, _: node,                                     # returns current node
        ".."    : lambda node, _: node.parent if node.parent else node,     # returns parent if exists, else just returns current node
        "**"    : lambda node, next_parts: node.map(lambda node: node.get(next_parts))    # implements recursive globbing
    }

    SPECIAL_PATH_FILE_RULES = dict()



    def __init__(self):

        """
        
        """