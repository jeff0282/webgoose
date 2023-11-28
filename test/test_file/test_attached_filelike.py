"""
Select Unit Tests for webgoose.filelike.FileLike

Test suite for a FileLike instance attached to a Component
"""

import  pytest

from    pytest_cases            import      parametrize_with_cases

from    webgoose                import      Component
from    webgoose.filelike       import      FileLike


@pytest.fixture
def single_component() -> Component:
    """
    An example component, unattached
    """
    return Component("test")


class SplitSlugCases:
    """
    FileLike attached with different slugs
    to stress FileLike's slug manipulation methods

    Cases return tuple in form:
    `(<test slug>, <expected dirname>, <expected basename>, <expected ext str>, <expected exts tuple>)`
    """
    
    def case_fname_single_ext(self):
        return "file.txt", "", "file", ".txt" , ("txt",)
    
    def case_fname_two_ext(self):
        return "archive.tar.gz", "", "archive", ".tar.gz", ("tar", "gz")

    def case_hidden_fname(self):
        return ".hidden", "", ".hidden", "", tuple()
    
    def case_path_single_ext(self):
        return "home/files/file.txt", "home/files", "file", ".txt", ("txt",)
    
    def case_path_two_ext(self):
        return "home/archive/word.docx.zip", "home/archive", "word", ".docx.zip", ("docx", "zip")
    
    def case_path_hidden_fname(self):
        return "home/hidden/.file", "home/hidden", ".file", "", tuple()
    
    def case_hidden_path(self):
        return "home/.hidden_path/file.txt", "home/.hidden_path", "file", ".txt", ("txt",)
        

# ---
# Test Attached Filelike
#

@parametrize_with_cases(["slug", "dirname", "basename", "ext_str", "ext_tuple"], cases=SplitSlugCases)
def test_attached_filelike(slug, dirname, basename, ext_str, ext_tuple, single_component):
    
    # create file and establish parent-child connection
    file = FileLike()
    single_component.add(slug, file)

    # Check methods against expected results
    assert file.parent == single_component
    assert file.parts == (single_component, file)
    assert file.path == slug
    assert file.dirname == dirname
    assert file.filename == basename + ext_str
    assert file.basename == basename
    assert file.ext == ext_str
    assert file.exts == ext_tuple




