
from    typing      import      Any
from    typing      import      Dict
from    typing      import      Optional
from    typing      import      Tuple
from    typing      import      Type


class Directory:

    """
    Primary node for webgoose site trees

    This class defines the doubly-linked, file system like
    tree that webgoose uses to build a site.
    """

    def __init__(self, 
                 name:      str, 
                 parent:    Optional[Type['Directory']]                             = None, 
                 children:  Optional[Tuple[Type['Directory'], Type[Renderable]]]    = tuple(),
                 metadata:  Optional[Dict[str, Any]]                                = dict(),
                 data:      Optional[Type[object]]                                  = None) -> None:
        
        """
        Create a directory node instance. Requires a name and parent.

        Can optionally take a Directory (or subclass) parent and subdirs, and children
        of type Renderable (or subclass)

        Also supports metadata and data arguments, which can be used for 
        arbitrary extensibility. Metadata dict is proxied as keys, data is available
        under the `.data` property
        """

        pass