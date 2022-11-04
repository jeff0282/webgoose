
import importlib
from webgoose import project_root
util = importlib.import_module('webgoose.util', "webgoose")


def test_validateURI():
    assert util.validateURI("^Dhg%$*&^%(!%$£)") == False
    assert util.validateURI("testint.page") == True
    assert util.validateURI("test^test.html") == True
    assert util.validateURI("jeff/one/two/three") == True
    assert util.validateURI("/jeff") == True
    assert util.validateURI("/") == True
    assert util.validateURI("") == True 
    assert util.validateURI("//") == False


def test_URIToRelativePath():
    assert util.URIToRelativePath("/") == "index"
    assert util.URIToRelativePath("") == "index"
    assert util.URIToRelativePath("/pages/") == "pages/index"
    assert util.URIToRelativePath("/pages") == "pages"
