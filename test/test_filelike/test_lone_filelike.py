"""
Select Unit Tests for webgoose.filelike.FileLike

Test suite for a FileLike instance with no `attach_point` set

Additionally includes tests that don't require an attach_point, like slug validation
"""

import  pytest

from    pytest_cases        import      parametrize_with_cases

from    webgoose.filelike   import      FileLike
from    webgoose.filelike   import      InvalidURIError
from    webgoose.filelike   import      URI


@pytest.fixture
def lone_filelike() -> FileLike:
    """
    A lone filelike instance with no parent

    (no parent = no attach point = no slug = no filename or anything)
    """
    return FileLike()


class SlugValidationCases:

    def fail_parent_dir_refs(self):
        return "this/../this/is/a/path"
    
    def fail_absolute_path(self):
        return "/this/is/an/absolute/path"
    
    def fail_malformed_absolute_path(self):
        return "/this/./is/a/path/"
    
    def fail_double_slashes(self):
        return "///this/is/a/malformed//path"
    
    def pass_current_dir_refs(self):
        return "this/./is/a/path/."


# ---
# Slug Validation
#
@parametrize_with_cases("slug", cases=SlugValidationCases, prefix="pass_")
def test_pass_slug_validation(slug):
    FileLike().validate_slug(URI(slug))


@parametrize_with_cases("slug", cases=SlugValidationCases, prefix="fail_")
def test_fail_slug_validation(slug):
    with pytest.raises(InvalidURIError):
        FileLike().validate_slug(URI(slug))


# ---
# Test Lone Filelike Methods
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

def test_lone_uri(lone_filelike: FileLike):
    assert lone_filelike.uri == "/"


