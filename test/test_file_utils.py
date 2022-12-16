
from webgoose.utils import file_utils


def test_split_filename():

    fname1 = "index.md"
    fname2 = "index."
    fname3 = "index"
    fname4 = "/home/user/webgoose/source/index.md"
    fname5 = ".md"
    fname6 = "/home/user/"

    assert file_utils.split_filename(fname1) == ('index', '.md')
    assert file_utils.split_filename(fname2) == ('index', '.')
    assert file_utils.split_filename(fname3) == ('index', '')
    assert file_utils.split_filename(fname4) == ('index', '.md')
    assert file_utils.split_filename(fname5) == ('', '.md')
    assert file_utils.split_filename(fname6) == ('', '')


