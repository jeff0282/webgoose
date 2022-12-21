
from webgoose.utils import file_utils


def test_map_path():

    """
    Tests for file_utils.map_path()
    """

    # The Test Cases
    # ---
    # Basic Case, Both Absolute
    test_path_1 = "/home/user/webgoose/source/index.md"
    test_source_1 = "/home/user/webgoose/source/"
    test_build_1 = "/home/user/webgoose/build/"

    # Case With SourceDir Missing Last Slash (may cause issues with os.path.join())
    test_path_2 = "/home/user/webgoose/source/index.md"
    test_source_2 = "/home/user/webgoose/source"
    test_build_2 = "/home/user/webgoose/build"

    # Case With Relative Source and Absolute Build
    test_path_3 = "./source/index.md"
    test_source_3 = "./source"
    test_build_3 = "/home/user/webgoose/build"

    # Case With Both Relative Source and Build
    test_path_4 = "./source/index.md"
    test_source_4 = "./source"
    test_build_4 = "./build"

    # Case With Source Path that Doesn't Contain Source Dir
    test_path_5 = "./source/index.md"
    test_source_5 = "./src"
    test_build_5 = "./bld"

    assert file_utils.map_path(test_source_1, test_build_1, test_path_1) == "/home/user/webgoose/build/index.md"
    assert file_utils.map_path(test_source_2, test_build_2, test_path_2) == "/home/user/webgoose/build/index.md"
    assert file_utils.map_path(test_source_3, test_build_3, test_path_3) == "/home/user/webgoose/build/index.md"
    assert file_utils.map_path(test_source_4, test_build_4, test_path_4) == "./build/index.md"
    assert file_utils.map_path(test_source_5, test_build_5, test_path_5) == False



def test_change_path_extension():

    """
    Tests for file_utils.change_path_extension()
    """

    # Standard Case
    test_path_1 = "/home/user/webgoose/.source/index.md"
    test_ext_1 = ".html"

    # Case Where Extension Has No Period Prefix
    test_path_2 = "/home/user/webgoose/.source/index.md"
    test_ext_2 = "html"

    # Error Case, Path Is Directory, So Return False
    test_path_3 = "/home/user/webgoose/.source/"
    test_ext_3 = ".html"

    assert file_utils.change_path_extension(test_path_1, test_ext_1) == "/home/user/webgoose/.source/index.html"
    assert file_utils.change_path_extension(test_path_2, test_ext_2) == "/home/user/webgoose/.source/index.html"
    assert file_utils.change_path_extension(test_path_3, test_ext_3) == False


