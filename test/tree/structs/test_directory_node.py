
"""
webgoose.tree.structs.DirNode (tests)

Tests for the site tree Directory Node, which implements the
full, doubly-linked tree functionality.
"""


def test_parts():

    """
    Test the .parts() method

    Should return a tuple containing all the elements
    between the current instance and root.
    
    Should return the below order:    
    (root, ... inbetween elements ... , instance)
    """

    


def test_path():

    """
    Test the .path() method

    Should return the complete path from instance
    to root, respecting anchoring, tree mounting,
    prefixes and delimiters, etc.
    """

    pass


def test_mount_unmount():

    """
    Test the ability to mount and unmount one tree
    to/from another.

    The 2 trees, when mounted, should act as one, but
    still be easily and cleanly seperated as required
    """

    pass


def test_rename():

    """
    Test ability to rename directories, renaming files must
    be done through the respective object.
    """


def test_delete():

    """
    Test ability to cleanly delete part or all of a tree
    """


def test_add():

    """
    Test ability to add files or directories to a file,
    and seperate them depending on the type of object.
    """

    pass


def test_get():

    """
    Test ability to get a child from current directory, or
    from any directory when given a path
    """

    pass


def test_glob():

    """
    Test glob functionality of directories.

    Matching is enabled through an external dependency,
    so this is not tested explicitly.
    """

    pass