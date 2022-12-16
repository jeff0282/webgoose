
from webgoose.base_page_querier import BasePageQuerier
from webgoose.structs import WGFile


def test_get_build_path():

    """
    Tests for BasePageQuerier._get_build_path()
    """

    # Initialise BasePageQuerier
    querier = BasePageQuerier()

    # Build Ext To Use
    build_ext = ".html"

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

    assert querier.get_build_path(test_source_1, test_build_1, test_path_1, build_ext) == "/home/user/webgoose/build/index.html"
    assert querier.get_build_path(test_source_2, test_build_2, test_path_2, build_ext) == "/home/user/webgoose/build/index.html"
    assert querier.get_build_path(test_source_3, test_build_3, test_path_3, build_ext) == "/home/user/webgoose/build/index.html"
    assert querier.get_build_path(test_source_4, test_build_4, test_path_4, build_ext) == "./build/index.html"
    assert querier.get_build_path(test_source_5, test_build_5, test_path_5, build_ext) == False



def test_add_default_metadata():

    # Initialise BasePageQuerier
    querier = BasePageQuerier()

    metadata = {'title': 'Title', 'description': ''}
    defaults = {'template': 'base.html', 'description': 'this is a description'}

    assert querier.add_default_metadata(metadata, defaults) == {'title': 'Title', 'description': '', 'template': 'base.html'}




