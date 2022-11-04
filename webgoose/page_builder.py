
import frontmatter, cmarkgfm, os, re
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader, select_autoescape
from webgoose.macro_processor import MacroProcessor
from cmarkgfm.cmark import Options as cmarkgfmOptions

import importlib
util = importlib.import_module('webgoose.util')        


class PageBuilder(object):


    TEMPLATE_LOCATION = os.path.join(os.getcwd(), "template")


    def __init__(self):
        pass


    def getPageData(self, filePath):
        with open(filePath, "r") as file:
            fileContent = frontmatter.load(file)
            return fileContent.metadata, fileContent.content



    def buildPage(self, filePath):

        # Get Page Metadata & Content
        meta, content = self.getPageData(filePath)

        # Convert Page Markdown To Markup
        body = self.convPageContent(filePath, content)

        # Use Body To Fill In Metadata Where Requires
        meta = self.checkAddMetadata(filePath, meta, body)

        # Render New Page Build
        render = self.render(meta, body)

        # Apply Macros, Use Beautiful Soup To Convert HTML Entities (necessary for macros)
        soup = BeautifulSoup(render, "html.parser")
        processor = MacroProcessor()
        finalMarkup = processor.processMacros(filePath, str(soup))

        # Use Beautiful Soup (again, I know it's bad) To Prettify HTML Before Output
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Beautiful soup should __NEVER__ convert &lt; and &gt; to < or > (WRITE UNIT TESTS TO CHECK)
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        soup = BeautifulSoup(finalMarkup, "html.parser")
        return soup.prettify(formatter="html")



    def render(self, meta, body):
        # Setup Jinja2 Environment
        jinjaEnv = Environment(
            loader=FileSystemLoader(self.TEMPLATE_LOCATION),
            autoescape=select_autoescape(
                enabled_extensions=('html', 'xml'),
                default_for_string=True,
            ))

        # Wrap Body in Jinja2 Tags, Create Jinja2 Template Object From String
        body = "{% extends 'default.html' %} {% block content %}" + re.sub("%", "&#37;", body) + "{% endblock %}"
        template = jinjaEnv.from_string(body)

        # Render Template, Pass Metadata Dict To Jinja2, Prettify Page (Fix Indentation, etc) and Return Result
        return template.render({"meta": meta})



    def checkAddMetadata(self, filePath, meta, body):
        htmlSoup = BeautifulSoup(body, "html.parser")

        if not "title" in meta:
            title = htmlSoup.find(re.compile("^h1$"))
            if title:
                meta['title'] = title.string
            else: 
                meta['title'] = util.getFilenameFromPath(filePath)

        if not "description" in meta:
            firstPara = htmlSoup.find("p")
            if firstPara:
                meta['description'] = firstPara.string[:80]
            else: 
                meta['description'] = "No Description Was Provided For This Page"

        if not "template" in meta:
            meta['template'] = "default.html"

        return meta
        
    

    def convPageContent(self, filePath, content):
        # Convert Markdown To HTML
        options = (cmarkgfmOptions.CMARK_OPT_UNSAFE)
        return cmarkgfm.github_flavored_markdown_to_html(content, options).strip()

