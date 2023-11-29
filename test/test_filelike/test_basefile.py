"""
Select Unit Tests for webgoose.filelike.BaseFile
"""

import  pytest

from    pytest_cases            import      parametrize_with_cases

from    webgoose.filelike       import      BaseFile
from    webgoose.filelike       import      InvalidPathError


class FnameValidationCases:

    def fail_directory_ending(self):
        return "invalid/"
    
    def fail_current_dir_ref(self):
        return "path/to/file/."
    
    def pass_hidden_file(self):
        return ".hidden"
    

# ---
# Test Filename Validation 
#

@parametrize_with_cases("slug", cases=FnameValidationCases, prefix="fail_")
def test_fail_fname_validation(slug):
    with pytest.raises(InvalidPathError):
        BaseFile().validate_slug(slug)


@parametrize_with_cases("slug", cases=FnameValidationCases, prefix="pass_")
def test_pass_fname_validation(slug):
    BaseFile().validate_slug(slug)
