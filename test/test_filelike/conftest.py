"""
General configuration for the Webgoose Test Suite
"""

import  pytest

from    webgoose.filelike   import      Component
from    webgoose.filelike   import      FileLike


@pytest.fixture
def lone_filelike() -> FileLike:
    """
    A lone filelike instance with no parent

    (no parent = no attach point = no slug = no filename or anything)
    """
    return FileLike()


@pytest.fixture
def plain_component() -> Component:
    """
    A standard component with nothing added

    Serves as a convenient anchor to attach things to
    """
    return Component("test")