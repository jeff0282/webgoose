
import frontmatter

from webgoose.base_page_querier import BasePageQuerier
from webgoose.structs import WGFile


# TEST FILES DIRECTORY (RELATIVE TO PROJECT ROOT)
TEST_FILES_DIR = "./webgoose/__test__/test_files/"


def test_get_build_path():

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

    assert querier._get_build_path(test_source_1, test_build_1, test_path_1, build_ext) == "/home/user/webgoose/build/index.html"
    assert querier._get_build_path(test_source_2, test_build_2, test_path_2, build_ext) == "/home/user/webgoose/build/index.html"
    assert querier._get_build_path(test_source_3, test_build_3, test_path_3, build_ext) == "/home/user/webgoose/build/index.html"
    assert querier._get_build_path(test_source_4, test_build_4, test_path_4, build_ext) == "./build/index.html"



def test_frontmatter_defaults():

    # Should Type Numbers Correctly, Content Should Be ''
    # (note space after 'Float: 5.5' (testing if it's stripped or interpreted as string))
    test_string_1 = "---\ntitle: Example Title\nInt: 5\nFloat: 5.5 \n---"

    # Content Should Be The String "1", Metadata {}
    test_string_2 = "1"

    # Content Should Be '', Metadata Should Be {}
    test_string_3 = ""

    # Misc Test, `template: Null` Should Return {'template: Null}
    test_string_4 = "---\ntemplate: Null\n---"


    # Test 1
    test1 = frontmatter.loads(test_string_1)
    assert test1.content == ''
    assert type(test1.metadata['Int']) == int
    assert type(test1.metadata['Float']) == float

    # Test 2
    test2 = frontmatter.loads(test_string_2)
    assert test2.content == "1"
    assert test2.metadata == {}

    # Test 3
    test3 = frontmatter.loads(test_string_3)
    assert test3.metadata == {}
    assert test3.content == ""

    # Test 4
    test4 = frontmatter.loads(test_string_4)
    assert test4.metadata['template'] == None



def test_add_default_metadata():

    # Initialise BasePageQuerier
    querier = BasePageQuerier()

    metadata = {'title': 'Title', 'description': ''}
    defaults = {'template': 'base.html', 'description': 'this is a description'}

    assert querier._add_default_metadata(metadata, defaults) == {'title': 'Title', 'description': '', 'template': 'base.html'}




