
import frontmatter
import yaml

def test_frontmatter_defaults():

    """
    Tests For External Python-Frontmatter Package

    Double-Checks Default Values
    """

    # Should Type Numbers Correctly, Content Should Be ''
    # (note space after 'Float: 5.5' (testing if it's stripped or interpreted as string))
    test_string_1 = "---\ntitle: Example Title\nInt: 5\nFloat: 5.5 \n---"

    # Content Should Be The String "1", Metadata {}
    test_string_2 = "1"

    # Content Should Be '', Metadata Should Be {}
    test_string_3 = ""

    # Misc Test, `template: Null` Should Return {'template: None}
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



def test_pyyaml_defaults():

    """
    Tests for External PYYAML Package 
    """

    test_string_1 = "title: "

    yaml_output = yaml.safe_load(test_string_1)
    assert yaml_output['title'] == None