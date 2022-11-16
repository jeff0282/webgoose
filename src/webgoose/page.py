
import os
import re
from typing import Dict, Tuple

import frontmatter

from src.webgoose.config import config



class PageException(Exception):

    def __init__(self, message="An Error Occured Getting Page Info"):
        self.__message = message

    def __str__(self):
        return self.__message





class Page():

    def __init__(self, source_path: str):

        self.__source_path = source_path






    def get_page(self):

        if self.is_source_path_valid():

            # Get Page Content And Metadata, Fill In Blanks If Necessary
            metadata, content = self.get_page_content()
            metadata = self.add_missing_metadata(metadata)


            # Build Dictionary Of Page Content
            page = {

                'source_path': self.__source_path,
                'build_path': self.get_build_path(),
                'filename': self.get_filename_from_path(),
                'template': self.get_template(metadata['template']),
                'metadata': metadata,
                'content': content

            }

            return page

        
        raise PageException(f"The Page At Path '{self.__source_path}' Does Not Exist")






    def get_page_content(self) -> Tuple[dict[str, str], str]:

        """
        Retrieves Markdown Content as 'str' and YAML Frontmatter as 'dict'
        From Source Markdown File
        """

        with open(self.__source_path, "r", encoding="utf-8") as file:
            data = frontmatter.load(file)

        return data.metadata, data.content







    def get_filename_from_path(self) -> str:

        """Gets Filename From Any Given Path"""


        # Get Index Of Last Slash In File Path, Returns -1 If None Exist
        last_slash_index = self.__source_path.rindex("/")

        # If Slash Found, Return Substring After It, Else Assume The Path Is The File Name
        return self.__source_path[last_slash_index+1:] if last_slash_index >= 0 else self.__source_path






    def get_build_path(self) -> str:

        BUILD_EXTENSION = ".html"

        # Get Source & Build Directories From Config
        source = config['build']['source-dir']
        build = config['build']['build-dir']

        # Replace Source Dir in Souce Path With Build Dir
        build_path = re.sub(f"^{source}", build, self.__source_path)

        # Replace File Extention With Build Extension
        return build_path.replace(".md", BUILD_EXTENSION)






    def add_missing_metadata(self, metadata: Dict[str, str]) -> Dict[str, str]:

        """Uses Content & Filename Of Page To Add Any Missing Metadata To Page"""

        # Set Title As Filename If Not Present In Metadata
        if not "title" in metadata:

            metadata["title"] = "No Title"


        # Set Template To Use To The Default Set In Config If Not Set
        if not "template" in metadata:

            metadata["template"] = config["build"]["default-template"]

        return metadata






    def get_template(self, template_name):

        if os.path.exists(f"template/{template_name}"):

            with open(f"template/{template_name}", 'r', encoding='utf-8') as file:
                return file.read()

        
        raise PageException(f"Template '{template_name}' Not Found For Page '{self.__source_path}'")






    def is_source_path_valid(self) -> bool:

        return (os.path.isfile(self.__source_path)) and (self.__source_path.endswith(".md"))