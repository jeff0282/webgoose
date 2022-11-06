
import os
import re
from typing import Dict, List, Tuple

import cmarkgfm
import frontmatter
from bs4 import BeautifulSoup
from cmarkgfm.cmark import Options as cmarkgfmOptions
from jinja2 import Environment, FileSystemLoader, select_autoescape

from src.webgoose.config import config
from src.webgoose.macro_processor import MacroProcessor


class PageBuilderException(Exception):
    pass


class PageBuilder():


    def __init__(self, pages_to_build: List[str]):
        self.to_build = pages_to_build




    def build_all(self):

        """
        Calls The Page Builder Method '__build()' For Every file_path 
        In The List Passed To The Page Builder Object
        """

        for page in self.to_build:
            self.__build(page)





    def __build(self, file_path: str):

        """Main Function To Build An Individual Page"""

        build_path = self.get_build_path(file_path)

        metadata, content = self.get_page_content(file_path)

        content = self.convert_content_to_markup(content)

        metadata = self.add_missing_metadata(build_path, metadata, content)

        page_build = self.render_template(metadata, content)

        post_processor = MacroProcessor(file_path, page_build)
        final = post_processor.process()

        self.write_build_to_file(build_path, final)





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





    def convert_content_to_markup(self, content: str) -> str:

        """Converts Markdown Documents (GitHub Flavoured) To HTML Markup"""

        options = cmarkgfmOptions.CMARK_OPT_UNSAFE

        return cmarkgfm.github_flavored_markdown_to_html(content, options)





    def add_missing_metadata(self, build_path: str, metadata: Dict[str, str], content: str) -> Dict[str, str]:

        """Uses Content & Filename Of Page To Add Any Missing Metadata To Page"""

        soup = BeautifulSoup(content, "html.parser")

        # Set Title As Either Value Of First 'h1' Tag or Filename (Last Resort) If Not Present
        if not "title" in metadata:

            title = soup.find("h1")

            if title:

                metadata["title"] = title.string

            else:

                metadata["title"] = self.get_filename_from_path(build_path)

        # Set Description To Value Of First 'p' Element If Not Present
        if not "description" in metadata:

            first_para = soup.find("p")

            if first_para:

                metadata["description"] = first_para.string[:80]

        # Set Template To Use To The Default Set In Config If Not Set
        if not "template" in metadata:

            metadata["template"] = config["build"]["default-template"]

        return metadata





    def render_template(self, metadata: Dict[str, str], content: str) -> str:

        """Insert Page Content Onto HTML Template And Renders Full HTML Document"""

        # Setup Jinja2 Environment
        jinja_env = Environment(
            loader = FileSystemLoader(config["build"]["template-location"]),
            autoescape = select_autoescape(
                enabled_extensions = ("html", "xml"),
                default_for_string = True
            ),
        )

        # Replace All Modulo Symbols With HTML Entity To Prevent Conflicts With Jinja2 Template Tags
        content = content.replace("%", "&#37;")

        # Wrap Page Content With Jinja2 Templating Tags, Create Template Object
        page_body = ("{% extends '" + metadata["template"] + "' %} {% block content %}" + content + "{% endblock %}")

        template = jinja_env.from_string(page_body)

        # Render Page, Pass Metadata Dict To Jinja2
        return template.render({"meta": metadata})
