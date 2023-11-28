"""
Select Unit Tests for webgoose.filelike.FileLike

Test suite for a FileLike instance attached to a Component
"""

from    pytest                  import      fixture
from    pytest_cases            import      parametrize_with_cases

from    webgoose                import      Component
from    webgoose.filelike       import      FileLike


@fixture
def single_component() -> Component:
    """
    An example component
    """
    return Component("test")


class AttachedSlugCases:
    """
    FileLike attached with different slugs
    to stress FileLike.basename, FileLike.ext & FileLike.exts methods

    Cases return tuple in form:
    `(<test slug>, <expected basename>, <expected ext str>, <expected exts tuple>)`
    """
    
    def case_fname_single_ext(self):
        return "file.txt","file", ".txt" , ("txt",)
    
    def case_fname_two_ext(self):
        return "archive.tar.gz", "archive", ".tar.gz", ("tar", "gz")

    def case_hidden_fname(self):
        return ".hidden", ".hidden", "", tuple()
    
    def case_path_single_ext(self):
        return "home/files/file.txt", "file", ".txt", ("txt",)
    
    def case_path_two_ext(self):
        return "home/archive/word.docx.zip", "word", ".docx.zip", ("docx", "zip")
    
    def case_path_hidden_fname(self):
        return "home/hidden/.file", ".file", "", tuple()
    
    def case_hidden_path(self):
        return "home/.hidden_path/file.txt", "file", ".txt", ("txt",)
        

# ---
# Test Attached Filelike
#

@parametrize_with_cases(["slug", "basename_str", "ext_str", "ext_tuple"], cases=AttachedSlugCases)
def test_attached_filelike(slug, basename_str, ext_str, ext_tuple, single_component):
    file = FileLike()
    single_component.add(slug, file)
    assert file.parent == single_component
    assert file.filename == basename_str + ext_str
    assert file.basename == basename_str
    assert file.ext == ext_str
    assert file.exts == ext_tuple




