
import frontmatter
import re

from typing import Tuple

from webgoose import config
from webgoose.structs import PageInfo
from webgoose.structs import WGFile




class PageQuerierException(WebgooseException):
    def __init__(self, message: Optional[str] = "There Was An Unexpected Error Retrieving A Page Source File"):
        super().__init__("PageQuerierException", message)



class PageQuerier:

    """
    PageQuerier

    A Class To Facillitate Gathering Of Information About Pages, When Provided A WGFile Object

    NOTE: It is assumed that the WGFile Instance Passed Upon Initialisation Is A Valid Markdown File
    """


    def __init__(self, wgfile_object: WGFile):

        """
        Instantiates An Instance of the PageQuerier Class With A WGFile Object
        """

        self.__file = wgfile_object



    @property
    def file(self) -> str:
        return self.__file



    def get_page_info(self) -> PageInfo:

        """
        # CALL METHODS THAT MAY POTENTIALLY THROW EXCEPTIONS #

        Returns A PageInfo Instance Containing All Information About A Page
        """

        if self.page_exists():

            # Get Raw Metadata and Content From Source File
            metadata, content = self._get_source_content()

            # Fill In Missing Metadata
            # (Adds Missing Info Like Title with Filename, Template with Default Path From Template, etc)
            metadata = self._add_missing_metadata()

            # Get Build Path 
            # (Uses Source Path and Root Build Path from Config)
            build_path = self._get_build_path()

            # Get Raw Template As String
            template = self._get_template(metadata['template'])

            # Create and Return A PageInfo Object Containing All Of The Gathered Info + WGFile Info
            return PageInfo(self.file.path, build_path, self.file.basename, self.file.extension, self.file.last_mod, metadata, template, content)

        else:

            raise PageQuerierException(f"The Page '{self.file.path}' Doesn't Exist or is Otherwise Inaccessable")



    def page_exists(self) -> bool:

        """
        Returns Boolean Of Whether A Path Exists and is a File
        """

        return os.path.isfile(self.file.path):



    def _get_build_path(self) -> str:

        """ Gets Build Path of Page Using Source Path as a Base """

        BUILD_EXTENSION = ".html"

        source_dir = config['build']['source-dir']
        build_dir = config['build']['build-dir']

        # Replace Source Dir In Source Path With Build Dir
        # (Preserves Directory Structure In Build Dir)
        build_path = re.sub(f"^{source_dir}", build_dir, self.file.path)

        # Change File Extension To Build Extension
        return re.sub(r"\.[\w]+$", BUILD_EXTENSION, build_path)



    def _get_template(self, template_path: str) -> str:

        """
        # THROWS AN EXCEPTION IF TEMPLATE FILE NOT FOUND #

        Gets Template File as String Using Path Provided
        """

        # Open Template Fole as UTF-8 Encoded Text File
        try:

            with open(template_path, "r", encoding="utf-8") as template:
                return template.read()

        except:

            # Raise A More Useful Exception Than FileNotFoundException
            raise PageGrabberException(f"The Template File '{template_path}', Used By Page '{self.file.path}' Either Doesn't Exist or is Otherwise Inaccessable")
        


    def _get_source_content(self) -> Tuple[dict[str, str], str]:

        """
        # WILL THROW EXCEPTION IF SOURCE FILE DOESN'T EXIST #

        Gets Source Content From File, Splits Metadata Into Dict and Content Into String
        Returns Tuple (metadata, content)
        """

        # Open File as UTF-8 Encoded Text File, Split YAML Frontmatter From Content 
        with open(self.file.path, "r", encoding="utf-8") as source:
            raw_content = frontmatter.load(source)

        # Set Default Values If Metadata or Content Otherwise Blank
        metadata = raw_content.metadata if raw_content.metadata else {}
        content = raw_content.content if raw_content.content else ""

        return metadata, content



    def _add_missing_metadata(self, metadata: dict[str, str]) -> dict[str, str]:

        """ 
        Fills In Missing Metadata Using Source File Informatation and Defaults
        """

        # Get Default Values, etc From Config
        default_template = config['build']['default-template']
        title_suffix = config['site']['title-suffix']

        # Add Title Metadata 
        if not "title" in metadata:

            # If No Title, Replace With Filename
            metadata['title'] = self.file.basename


        # Add Title Suffix To Title (add space between)
        metadata['title'] += " " + title_suffix

        # If No Template Specified, Choose Default
        if not "template-path" in metadata:

            metadata['template-path'] = default_template


        return metadata