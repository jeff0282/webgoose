
"""
webgoose.tree.node

Contains implementations of the nodes that make up the webgoose
build tree.

These classes are designed to be built upon to cater to user's needs, however
generic classes are offered which provide necessary functionality.

Custom classes should inherit from one of these generic classes
"""

from    .base_node          import      BaseNode
from    .generic_directory  import      GenericDirectory
#from    .generic_file       import      GenericFile
