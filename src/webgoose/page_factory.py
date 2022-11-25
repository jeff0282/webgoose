
import os
import re
import frontmatter
from typing import Tuple

from src.webgoose.config import config
from src.webgoose.webgoose_exception import WebgooseException




class PageFactoryException(WebgooseException):

    def __init__(self, message="An Error Occured While Gathering Information From A Page"):
        super().__init__("PageFactoryException", message)




class PageFactory():



    class Page():

        def __init__(self, source_path: str, build_path: str, filename: str, metadata: dict[str, str], content: str, template: str):

            """ Initialises Page Object With All Page Information, Sourced By PageFactory """

            # Mutable
            self.content = content
            self.template = template

            # Immutable
            self._metadata = metadata
            self._filename = filename
            self._source_path = source_path
            self._build_path = build_path


        @property
        def metadata(self) -> str:
            return self._metadata


        @property
        def filename(self) -> str:
            return self._filename


        @property
        def source_path(self) -> str:
            return self._source_path


        @property
        def build_path(self) -> str:
            return self._build_path




    def __init__(self, source_path: str):

        """ Initialise PageFactory Instance With A File Path to the Source Markdown File """

        self._source_path = source_path




    # ==============
    # Public Methods
    # ==============

    @property
    def source_path(self):
        return self._source_path 



    def get_page(self) -> PageFactory.Page:

        """
        Returns A ReadOnly Page Object Containing All Page Information
        """

        if self.__source_file_valid():

            # Get Content From Source File
            metadata, content = self._get_source_content()

            # Get Build Path and Filename
            build_path = self._get_build_path()
            filename = self._get_filename()

            # Fill In Missing Metadata
            metadata = self._add_missing_metadata(filename, metadata)

            # Get Template From Name Provided In Metadata
            template = self._get_template(metadata['template-path'])

            return PageFactory.Page(self._source_path, build_path, filename, metadata, content, template)

        else:

            raise PageFactoryException(f"The Page '{self._source_path}' Could Not Be Loaded As It's Either Invalid or Doesn't Exist")




    # ===============
    # Private Methods
    # ===============

    def _get_source_content(self) -> Tuple[dict, str]:

        """ 
        # THROWS EXCEPTION IF SOURCE FILE DOESN'T EXIST #
        # (get_page() SHOULD CHECK BEFORE CALLING THIS FUNCTION) #
        Apply Frontloader to Source File To Get Content and Metadata Dict """

        with open(self._source_path, "r", encoding="utf-8") as source_file:
            full_page = frontmatter.load(source_file)

        # Empty Files May Result In Content and Metadata Being None
        metadata = full_page.metadata if full_page.metadata else {}
        content = full_page.content if full_page.content else ""

        return metadata, content




    def _get_template(self, template_name: str) -> str:

        """ 
        # THROWS EXCEPTION ON SOURCE FILE NOT EXISTING, OR FAILURE TO READ #
        Gets Template From Metadata (or use default), Return as String 
        """

        template_path = os.path.join(config['build']['template-dir'], template_name)

        with open(template_path, "r", encoding="utf-8") as template_file:

            return template_file.read()




    def _get_filename(self) -> str:

        """ 
        # SOURCE PATH SHOULD BE A FILE - get_page() SHOULD CHECK BEFORE CALLING THIS #
        Extracts Filename from Source Path 
        !! DISCARDS FILE EXTENSION !!
        """

        # Set Initial Value For Filename
        # (assume path is filename until proven otherwise)
        filename = self._source_path

        # Get Index of Last Slash, Returns -1 If None Found
        last_slash_index = filename.rindex("/")

        # Return Everything After Last Slash In Source Path
        if not last_slash_index == -1:
            filename = filepath[last_slash_index:]

        # Strip Off File Extension and Return
        return re.sub(r"\.[\w]$", "", filename)
        
    


    def _get_build_path(self) -> str:

        """ Gets Build Path of Page Using Source Path as a Base """

        BUILD_EXTENSION = ".html"

        source_dir = config['build']['source-dir']
        build_dir = config['build']['build-dir']

        # Replace Source Dir In Source Path With Build Dir
        # (Preserves Directory Structure In Build Dir)
        build_path = re.sub(f"^{source_dir}", build_dir, self._source_path)

        # Change File Extension To Build Extension
        return re.sub(r"\.[\w]+$", BUILD_EXTENSION, build_path)




    def _add_missing_metadata(self, filename: str, metadata: dict) -> dict:

        """ Fills In Missing Metadata Using Source File Informatation and Defaults """

        # Get Default Values, etc From Config
        default_template = config['build']['default-template']
        title_suffix = config['site']['title-suffix']

        # Add Title Metadata 
        if not "title" in metadata:

            # If No Title, Replace With Filename
            metadata['title'] = filename


        # Add Title Suffix To Title (add space between)
        metadata['title'] += " " + title_suffix

        # If No Template Specified, Choose Default
        if not "template-path" in metadata:

            metadata['template-path'] = default_template


        return metadata




    def _source_file_valid(self) -> bool:

        """ Returns a Bool Indicating Whether or Not The Source File Exists and is Valid (has '.md' Extension) """

        if os.path.isfile(self._source_path):

            return self._source_path.endswith(".md")

        return False
    


