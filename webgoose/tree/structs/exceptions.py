
"""
webgoose.tree.structs.exceptions

Exceptions for use by webgoose site tree nodes
"""


class DuplicateChildNameError(Exception):
    """ 
    Directory node already has a child with a matching name

    To be used when encountering a naming conflict
    """
    pass



class InvalidNameError(Exception):
    """
    Node name provided is invalid or otherwise unusable
    """
    pass



class InvalidParentError(Exception):
    """
    Provided parent node cannot be used as a parent
    """
    pass



class NodeNotFoundError(Exception):
    """
    Node at given path is not found    
    """
    pass