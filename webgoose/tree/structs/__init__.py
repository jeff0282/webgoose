
"""
webgoose.tree.structs

The structs submodule for Webgoose trees, containing all built-in tree nodes
"""

# Exception Classes

from    .exceptions     import      DuplicateChildNameError
from    .exceptions     import      InvalidNameError
from    .exceptions     import      InvalidParentError
from    .exceptions     import      NodeNotFoundError


# Node Classes
from    .tree_node      import      TreeNode
from    .dir_node       import      Directory