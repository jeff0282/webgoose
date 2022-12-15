
import os

from typing import Tuple, Optional

from webgoose import config
from webgoose import WebgooseException
from webgoose.base_page_querier import BasePageQuerier
from webgoose.structs import PageInfo
from webgoose.structs import WGFile


#
# Constant 
#
BUILD_EXTENSION = ".html"



class PageQuerierException(WebgooseException):
    def __init__(self, message: Optional[str] = "There Was An Unexpected Error Retrieving A Page Source File"):
        super().__init__("PageQuerierException", message)



class PageQuerier(BasePageQuerier):

    """
    PageQuerier

    A Class To Facillitate Gathering Of Information About Pages, When Provided A WGFile Object

    NOTE: It is assumed that the WGFile Instance Passed Upon Initialisation Is For A Valid Markdown File
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
            metadata, content = self.get_source()

            # Fill In Missing Metadata
            # (Adds Missing Info Like Title with Filename, Template with Default Path From Template, etc)
            metadata = self.add_missing_metadata(metadata)

            # Get Build Path 
            # (Uses Source Path and Root Build Path from Config)
            build_path = self.get_build_path()

            # Get Raw Template As String
            template = self.get_template(metadata['template'])

            # Create and Return A PageInfo Object Containing All Of The Gathered Info + WGFile Info
            return PageInfo(self.file.path, build_path, self.file.basename, BUILD_EXTENSION, self.file.last_mod, metadata, template, content)

        else:

            raise PageQuerierException(f"The Page '{self.file.path}' Doesn't Exist or is Otherwise Inaccessable")


    
    def page_exists(self) -> bool:

        """
        Returns Boolean Of Whether Page Exists Or Not

        The Definition of a Valid Page May Be Expanded Upon In Future, Hence Exists A Dedicated Method
        """

        return os.path.isfile(self.file.path)



    def get_build_path(self) -> str:

        """ 
        # THROWS EXCEPTION IF SOURCE_PATH DOESN'T CONTAIN SOURCE_DIR #

        Gets Build Path of Page Using Source Path as a Base

        Uses The BasePageQuerier's `_get_build_path()` To Do The Actual Conversion
        """

        source_dir = config['build']['source_dir']
        build_dir = config['build']['build_dir']

        build_path = super().get_build_path(source_dir, build_dir, self.file.path, BUILD_EXTENSION)

        # Check If Build_Path is False (source_path doesn't contain source_dir)
        if build_path:

            return build_path

        else:

            raise PageQuerierException(f"The Source File With Path '{self.file.path}' is NOT in Source Dir '{source_dir}'")



    def get_template(self, template_path: str) -> str:

        """
        # THROWS AN EXCEPTION IF TEMPLATE FILE NOT FOUND #

        Gets Template File as String Using Path Provided
        """

        # Get Template Dir from Config, Concatenate It To Relative TemplatePath
        # (Strips '/' From Start Of 'template_path' If Present To Prevent 'os.path.join()' Issues)
        template_dir = config['build']['template_dir']
        template_path = template_path[1:] if template_path[0] == "/" else template_path
        template_path = os.path.join(template_dir, template_path)

        # Get Template Using BasePageQuerier Method
        template = super().get_template(template_path)

        # Check If _get_template() Returned False, Throw Exception
        if template:

            return template

        else:
        
            raise PageQuerierException(f"The Template File '{template_path}', Used By Page '{self.file.path}' Either Doesn't Exist or is Otherwise Inaccessable")
        


    def get_source(self) -> Tuple[dict[str, str], str]:

        """
        # WILL THROW EXCEPTION IF SOURCE FILE DOESN'T EXIST #

        Gets Source Content From File, Splits Metadata Into Dict and Content Into String
        Returns Tuple (metadata, content)
        """

        # Get Source Using BasePageQuerier
        # _get_source() Returns The Tuple (metadata, content) or False on failure
        source = super().get_source(self.file.path)

        # Check If BasePageQuerier Returned False
        if source:
            
            return source[0], source[1]

        else:

            raise PageQuerierException(f"The Source File For The Page'{self.file.path} Either Doesn't Exist or Is Inaccessable")



    def add_missing_metadata(self, metadata: dict[str, str]) -> dict[str, str]:

        """ 
        Fills In Missing Metadata Using Source File Informatation, config, and Defaults
        """

        # Get Default Values, etc From Config
        default_template = config['build']['default_template']
        title_suffix = config['site']['title_suffix']
        
        # Populate Dict To Be Passed To BasePageQuerier Method
        default_values = {'title': self.file.basename, 'template': default_template}
        metadata = super().add_default_metadata(metadata, default_values)

        # Add Title Suffix To Title
        metadata['title'] = f"{metadata['title']} {title_suffix}"

        return metadata