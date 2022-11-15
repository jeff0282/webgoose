
import os
import re
from typing import Dict, List, Tuple

import cmarkgfm
import frontmatter
from bs4 import BeautifulSoup
from cmarkgfm.cmark import Options as cmarkgfmOptions
from jinja2 import Environment, FileSystemLoader

from src.webgoose.config import config
from src.webgoose.macro_processor import MacroProcessor





class PageBuilder():


    def __init__(self, pages_to_build: List[str]):

        self.build_list = pages_to_build




    def build_all(self):

        """
        Calls The Page Builder Method '__build()' For Every file_path 
        In The List Passed To The Page Builder Object
        """

        for file_path in self.build_list:
            
            page_build = self.__build_page(file_path)

            build_path = self.get_build_path(file_path)

            self.write_build_to_file(build_path, page_build)






    def __build_page(self, file_path: str):

        """Main Function To Build An Individual Page"""

        metadata, content = self.get_page_content(file_path)
        
        metadata = self.add_missing_metadata(file_path, metadata)

        template = self.get_template(metadata['template'])

        template, content = self.process_macros(file_path, template, content)

        content = self.conv_markdown_html(content)

        return self.render_template(template, metadata, content)






    def get_build_path(self, file_path: str) -> str:

        """Work Out Build Path From Any Given Markdown Source Path"""

        EXTENSION = ".html"

        # Replace Source Directory with Build Directory
        match_string = f"^{config['build']['source-dir']}"

        repl_string = config["build"]["build-dir"]

        build_path = re.sub(match_string, repl_string, file_path)

        # Replace From Last Occurence of '.' In String Till End With Build Extension
        last_period_index = build_path.rindex(".")

        # rindex() Returns -1 If No Occurence Found
        if last_period_index > 0:

            return build_path[:last_period_index] + EXTENSION

        return build_path + EXTENSION






    def get_filename_from_path(self, file_path: str) -> str:

        """Gets Filename From Any Given Path"""

        last_slash_index = file_path.rindex("/")

        # Return Substring After Last Slash If Present, Else Returns Path
        return file_path[:last_slash_index] if last_slash_index > 0 else file_path






    def get_page_content(self, file_path: str) -> Tuple[dict[str, str], str]:

        """
        Retrieves Markdown Content as 'str' and YAML Frontmatter as 'dict'
        From file_path Specified
        """

        with open(file_path, "r", encoding="utf-8") as file:
            data = frontmatter.load(file)

        return data.metadata, data.content






    def write_build_to_file(self, build_path: str, page_build: str):

        """Write Final HTML Output For A Page To File"""

        if not os.path.exists(os.path.dirname(build_path)):

            os.makedirs(os.path.dirname(build_path))


        with open(build_path, "w", encoding="utf-8") as file:

            soup = BeautifulSoup(page_build, "html.parser")

            file.write(soup.prettify(formatter="html"))






    def process_macros(self, file_path, template, content):

        # Process Macros On Page Content
        pre_processor = MacroProcessor(file_path, content)
        
        content = pre_processor.process()

        
        # Process Macros On Template, Using Content As Reference
        pre_processor = MacroProcessor(file_path, template, content)

        template = pre_processor.process()


        return template, content 





    def conv_markdown_html(self, content: str) -> str:

        """
        Converts Markdown Documents (GitHub Flavoured) To HTML Markup
        """

        # Convert Markdown to HTML, Use Safe Formatting To Avoid Injection/XSS Issues
        cmark_options = cmarkgfmOptions.CMARK_OPT_UNSAFE

        return cmarkgfm.github_flavored_markdown_to_html(content, cmark_options)





    def add_missing_metadata(self, build_path: str, metadata: Dict[str, str]) -> Dict[str, str]:

        """Uses Content & Filename Of Page To Add Any Missing Metadata To Page"""

        # Set Title As Filename If Not Present In Metadata
        if not "title" in metadata:

            metadata["title"] = self.get_filename_from_path(build_path)


        # Set Template To Use To The Default Set In Config If Not Set
        if not "template" in metadata:

            metadata["template"] = config["build"]["default-template"]

        return metadata





    def get_template(self, template_name):

        if os.path.exists(f"template/{template_name}"):

            with open(f"template/{template_name}", 'r', encoding='utf-8') as file:
                
                return file.read()

        else:

            return False





    def render_template(self, template, metadata: Dict[str, str], content: str) -> str:

        """Insert Page Content Onto HTML Template And Renders Full HTML Document"""

        # Setup Jinja2 Environment
        jinja_env = Environment(
            loader=FileSystemLoader("template")
        )

        # Replace All Modulo Symbols With HTML Entity To Prevent Conflicts With Jinja2 Template Tags
        content = content.replace("%", "&#37;")

        # Create Template Object From Template String
        template = jinja_env.from_string(template)

        # Render Page, Pass Metadata Dict To Jinja2, Process Macros On Template
        full_page = template.render({"meta": metadata, "content": content})
        return full_page
