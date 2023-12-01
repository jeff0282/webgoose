"""
Select Unit Tests for webgoose.filelike.component
"""

import  pytest

from    webgoose.filelike       import      Component
from    webgoose.filelike       import      FileLike
from    webgoose.filelike       import      NotAnOrphanError

# ---
# SINGLE UNIT TESTS
#

@pytest.fixture
def component():
    return Component("test")


def test_add_file(component):
    f = FileLike()
    component.add("file.txt", f)
    assert f in component
    assert f.parent == component
    assert f.slug == "file.txt"


def test_duplicate_slug_add(component):
    f = FileLike()
    f2 = FileLike()
    component.add("file.txt", f)
    with pytest.raises(FileExistsError):
        component.add("file.txt", f2)


def test_duplicate_obj_add(component):
    f = FileLike()
    component.add("file.txt", f)
    with pytest.raises(NotAnOrphanError):
        component.add("file.duplicate", f)

