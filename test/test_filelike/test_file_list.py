"""
Select Unit Tests for webgoose.filelike.FileList
"""

from    pytest_cases    import      parametrize_with_cases

from    webgoose.filelike       import      FileLike
from    webgoose.filelike       import      FileList

glob_std_test = {

}

class FileListGlobCases:
    def case_recursive_dif_levels(self):
        return "**/*.html", [
            "blog/posts/post1.html",
            "blog/posts/post2.html",
            "blog/posts/post3.html",
            "blog/articles/article1.html",
            "blog/articles/article2.html",
            "blog/tags.html"
        ]
    
    def case_std_no_dif_levels(self):
        return "*/*/*.html", [
            "blog/posts/post1.html",
            "blog/posts/post2.html",
            "blog/posts/post3.html",
            "blog/articles/article1.html",
            "blog/articles/article2.html",
        ]

@parametrize_with_cases(["glob_exp","uri_strs"], cases=FileListGlobCases)
def test_glob_recursive(glob_exp: str, uri_strs: list[str]):
    #TODO: CHANGE THIS FILELIKE TO COMPONENT
    root = FileLike()
    fl = FileList()
    for uri in uri_strs:
        child = FileLike()
        child.set_attach_point(slug_str=uri, parent=root, is_index=None)
        fl.add(child)

    for file in fl.glob(glob_exp):
        assert 
        uri_strs.pop(uri_strs.index(uri))

    assert uri_strs == []

    

    

