
import frontmatter
import re

from typing import Tuple

from webgoose import config


class PageGrabberException(WebgooseException):
    def __init__(self, message: Optional[str] = "There Was An Unexpected Error Retrieving A Page Source File"):
        super().__init__("PageGrabberException", message)



class PageGrabber:

    """
    PageGrabber - Grabs All Information About A Page, Returns A PageInfo Object

    NOT FOR EXTERNAL USE:
    There Exists A Subclass, PageQuerier, Designed For External Use.
    """


    class PageInfo:

        """
        PageInfo - A Read-Only Struct For Storing Page Information Provided By PageGrabber
        """

        def __init__(self, source_path: str, build_path: str, last_mod_time: float,
                    metadata: dict[str, str], template: str, content: str,):

            """
            Initialise PageInfo Object With All Page Information Provided
            """

            # Source File Info
            self.__source_path = source_path
            self.__build_path = build_path
            self.__last_mod = last_mod_time
            
            # Source File Contents
            self.__metadata = metadata
            self.__content = content

            # Info Derived From Source File
            self.__template = template



        @property
        def source_path(self) -> str:
            return self.__source_path

        @property
        def build_path(self) -> str:
            return self.__build_path

        @property
        def last_mod(self) -> float:
            return self.__last_mod

        @property
        def meta(self) -> dict[str, str]:
            return self.__metadata

        @property
        def raw_content(self) -> str:
            return self.__content

        @property
        def raw_template(self) -> str:
            return self.__template




    def __init__(self, source_path: str):

        """
        Instantiates An Instance of the PageGrabber Class With A Page Location
        """

        self.__source_path = source_path



    @property
    def source_path(self) -> str:
        return self.__source_path



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

            # Get Last Modified Date As Epoch Timestamp
            last_mod_time = os.path.getmtime(self.source_path)

            # Create and Return A PageInfo Object Containing All Of The Gathered Info
            return PageInfo(self.source_path, build_path, last_mod_time, metadata, template, content)

        else:

            raise PageGrabberException(f"The Page '{self.source_path}' Doesn't Exist or is Otherwise Inaccessable")



    def page_exists(self) -> bool:

        """
        Returns Boolean Of Whether A Path Exists and is a File
        """

        return os.path.isfile(self.source_path):



    def _get_build_path(self) -> str:

        """ Gets Build Path of Page Using Source Path as a Base """

        BUILD_EXTENSION = ".html"

        source_dir = config['build']['source-dir']
        build_dir = config['build']['build-dir']

        # Replace Source Dir In Source Path With Build Dir
        # (Preserves Directory Structure In Build Dir)
        build_path = re.sub(f"^{source_dir}", build_dir, self.source_path)

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
            raise PageGrabberException(f"The Template File '{template_path}', Used By Page '{self.source_path}' Either Doesn't Exist or is Otherwise Inaccessable")
        


    def _get_source_content(self) -> Tuple[dict[str, str], str]:

        """
        # WILL THROW EXCEPTION IF SOURCE FILE DOESN'T EXIST #

        Gets Source Content From File, Splits Metadata Into Dict and Content Into String
        Returns Tuple (metadata, content)
        """

        # Open File as UTF-8 Encoded Text File, Split YAML Frontmatter From Content 
        with open(self.source_path, "r", encoding="utf-8") as source:
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
            metadata['title'] = os.path.basename(self.source_path)


        # Add Title Suffix To Title (add space between)
        metadata['title'] += " " + title_suffix

        # If No Template Specified, Choose Default
        if not "template-path" in metadata:

            metadata['template-path'] = default_template


        return metadata