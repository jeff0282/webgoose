
from    webgoose.tree.structs   import      Directory


class Anchor(Directory):

    """
    A special type of Node for use as the root of webgoose directory trees

    Extends the Directory Class, implementing special behaviours such as 
    standardised root naming, and mounting/unmounting subtrees.
    """

    def __init__(self, 
                 children:  Optional[Tuple[Type['Directory'], Type[Renderable]]]    = tuple(),
                 metadata:  Optional[Dict[str, Any]]                                = dict(),
                 data:      Optional[Type[object]]                                  = None) -> None:
        
        """
        Create an anchor node instance, for use as root of webgoose directory tree.

        Takes no name or parent directly; this is handled exclusively by mounting and unmounting.
        """

        