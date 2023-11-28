"""
Unit Tests for webgoose.struct.file.FileLike
"""

import  pytest

from    webgoose             import      Component
from    webgoose.filelike    import      FileLike


def filelike_in_component(slug: str) -> FileLike:
    """
    Create a filelike object with a component parent

    Slug and parent are only set when attached to a parent
    Components are pretty much a poorman's directory
    """

    parent = Component("parent")
    child = FileLike(slug)
    parent.add(slug, child)
    return child


@pytest.fixture
def lone_filelike() -> FileLike:
    """
    A lone filelike instance with no parent

    (no parent = no attach point = no slug = no filename or anything)
    """

    return FileLike()


# ---
# TEST LONE FILELIKE
#

def test_lone_slug(lone_filelike: FileLike):
    assert lone_filelike.slug == ""

def test_lone_parent(lone_filelike: FileLike):
    assert lone_filelike.parent == None

def test_lone_attach_point(lone_filelike: FileLike):
    assert lone_filelike.attach_point == None

def test_lone_filename(lone_filelike: FileLike):
    assert lone_filelike.filename == ""

def test_lone_ext(lone_filelike: FileLike):
    assert lone_filelike.ext == ""

def test_lone_exts(lone_filelike: FileLike):
    assert lone_filelike.exts == tuple()

def test_lone_dirname(lone_filelike: FileLike):
    assert lone_filelike.dirname == ""

def test_lone_basename(lone_filelike: FileLike):
    assert lone_filelike.basename == ""

def test_lone_parts(lone_filelike: FileLike):
    assert lone_filelike.parts == (lone_filelike,)

def test_lone_path(lone_filelike: FileLike):
    assert lone_filelike.path == ""


