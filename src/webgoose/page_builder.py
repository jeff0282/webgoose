
import os
import re
from typing import Dict, List, Tuple

import cmarkgfm
from bs4 import BeautifulSoup
from cmarkgfm.cmark import Options as cmarkgfmOptions
from jinja2 import Environment, FileSystemLoader

from src.webgoose.config import config
from src.webgoose.page import Page
from src.webgoose.macro_processor import MacroProcessor


class PageBuilder():


    def __init__(self, pages_to_build: List[str]):

        self.build_list = pages_to_build




    def build_all(self):

        """
        Calls The Page Builder Method '__build()' For Every file_path 
        In The List Passed To The Page Builder Object
        """

        # Build All Pages Provided In List
        built_pages = [self.__build_page(file_path) for file_path in self.build_list]


        # Check If Anything Failed To Build
        if False in built_pages:
            print("Some Pages Failed To Build")





    def __build_page(self, file_path: str):

        """Main Function To Build An Individual Page"""

        # [Terrible Naming]
        # Construct Page Object Using Source Path, Get All Page Content Using It (dict)
        page_parser = Page(file_path)
        page_dict = page_parser.get_page()

        page_dict = self.process_macros(page_dict)

        page_dict['content'] = self.conv_markdown_html(page_dict['content'])

        build = self.render_page(page_dict)

        self.write_build_to_file(page_dict['build_path'], build)






    def write_build_to_file(self, build_path: str, build: str):

        """Write Final HTML Output For A Page To File"""


        if not os.path.exists(os.path.dirname(build_path)):

            os.makedirs(os.path.dirname(build_path))


        with open(build_path, "w", encoding="utf-8") as file:

            soup = BeautifulSoup(build, "html.parser")

            file.write(soup.prettify(formatter="html"))






    def process_macros(self, page_dict: dict) -> dict:

        # Process Macros On Page Content
        pre_processor = MacroProcessor(page_dict, page_dict['content'])
        page_dict['content'] = pre_processor.process()

        
        # Process Macros On Template, Using Content As Reference
        pre_processor = MacroProcessor(page_dict, page_dict['template'], page_dict['content'])
        page_dict['template'] = pre_processor.process()


        return page_dict





    def conv_markdown_html(self, content: str) -> str:

        """
        Converts Markdown Documents (GitHub Flavoured) To HTML Markup
        """

        # Convert Markdown to HTML, Use Unsafe Formatting 
        # (files are generated once locally, so no real issues with XSS, etc)
        cmark_options = cmarkgfmOptions.CMARK_OPT_UNSAFE
        return cmarkgfm.github_flavored_markdown_to_html(content, cmark_options)





    def render_page(self, page_dict: dict) -> str:

        """Insert Page Content Onto HTML Template And Renders Full HTML Document"""

        # Setup Jinja2 Environment
        jinja_env = Environment(
            loader=FileSystemLoader("template")
        )

        # Replace All Modulo Symbols With HTML Entity To Prevent Conflicts With Jinja2 Template Tags
        page_dict['content'] = page_dict['content'].replace("%", "&#37;")

        # Create Template Object From Template String
        template = jinja_env.from_string(page_dict['template'])

        # Render Page, Pass Metadata Dict To Jinja2, Process Macros On Template
        return template.render({"meta": page_dict['metadata'], "content": page_dict['content']})
