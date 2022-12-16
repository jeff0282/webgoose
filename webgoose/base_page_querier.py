
import frontmatter
import os
import re

from typing import Any, Dict, Tuple, Union

class BasePageQuerier:

    """

    # BasePageQuerier:

    Implements The Logic Of The PageQuerier Class

    All Methods Here Take Their Arguments Seperately, No Data Is Stored Within Instances

    This Class Is To Be Inheritted By PageQuerier, Which Should Store Information, Provide Default Values,
    and Catch Exceptions

    ---

    # Justification for the Seperation:

    The Seperation Of All Logic To This Class Allows For Methods To Be More Easily Tested, Without Having
    To Worry About Providing Dummy Config Files, WGFile Instances, etc

    """

    def __init__(self):

        """
        No Data Is Stored Within This Class

        Nothing To Declare/Initialise
        """
        pass



    def get_build_path(self, source_dir: str, build_dir: str, source_path: str, build_extension: str) -> Union[str, bool]:

        """
        Converts a SourceFile Path to a Path Within The BuildDir, Respecting Folder Structure Of SourceDir

        Returns 'False' If SourceDir is not within SourcePath
        """

        # Test Whether SourceDir is a prefix of SourcePath
        if os.path.commonprefix([source_dir, source_path]) != source_dir:
            return False

        # Replace Source Dir In Source Path With Build Dir
        # Strip Source Dir From Source Path, Put Build_Dir At Front
        rel_build_path = re.sub(r"^"+source_dir, "", source_path)

        # Strip Off First '/' If Present To Avoid os.path.join() issues
        build_path = rel_build_path[1:] if rel_build_path[0] == "/" else rel_build_path
        build_path = os.path.join(build_dir, build_path)

        # Change File Extension To Build Extension
        return re.sub(r"\.[\w]+$", build_extension, build_path)


    
    def get_template(self, template_path: str) -> Union[str, bool]:

        """
        Get Template From Path Provided As A String

        If TemplatePath is "Null", Return The Empty Template

        Returns 'False' If Template Not Found
        """

        # Strip Whitespace To Avoid Comparison Issues
        template_path = template_path.strip()

        # Return Empty Template If Path is None
        if template_path == None:

            return "{{content}}"

        # If Not "None" Check If File Exists
        elif os.path.isfile(template_path):

            with open(template_path, "r", encoding="utf-8") as template:
                return template.read()

        # If Specified Template Doesn't Exist, Return None
        else:

            return False



    def get_source(self, source_path: str) -> Union[Tuple[Dict[str,Any], str], bool]:

        """
        Read Source File, Split Frontmatter from Content

        Returns 'False' If File Doesn't Exist
        """

        if os.path.isfile(source_path):

            # Open File as UTF-8 Encoded Text File, Split YAML Frontmatter From Content 
            with open(source_path, "r", encoding="utf-8") as source:
                raw_source = frontmatter.load(source)
                return raw_source.metadata, raw_source.content

        else:

            return False



    def add_default_metadata(self, metadata: dict[str, Any], default_values: dict[str, Any]) -> Dict[str, Any]:

        """
        Takes A Dictionary of Default Values, Inserts Into Metadata Dict If Not Present
        """

        # Loop Through Default Values, Add To Metadata If Value Not Present
        for key, value in default_values.items():

            if not key in metadata:

                metadata[key] = value

        return metadata






