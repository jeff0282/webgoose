
import frontmatter, cmarkgfm, jinja2, os, re
from bs4 import BeautifulSoup
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

        # Generate Body Content
        body = self.processPageContent(filePath, content)

        # Use Body To Fill In Metadata Where Requires
        meta = self.checkAddMetadata(filePath, meta, body)

        # Render New Page Build
        return self.render(meta, body)



    def render(self, meta, body):
        # Setup Jinja2 Environment
        jinjaEnv = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.TEMPLATE_LOCATION)
        )

        # Wrap Body in Jinja2 Tags, Create Jinja2 Template Object From String
        body = "{% extends 'default.html' %} {% block content %}" + body + "{% endblock %}"
        template = jinjaEnv.from_string(body)

        # Render Template, Pass Metadata Dict To Jinja2, Prettify Page (Fix Indentation, etc) and Return Result
        render = template.render({"meta": meta})
        htmlSoup = BeautifulSoup(render, "html.parser")
        return htmlSoup.prettify()



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
        
    

    def processPageContent(self, filePath, content):
        # Process Macros 
        processor = MacroProcessor(filePath, content)
        processedMarkdown = processor.processMacros()

        # Convert Markdown To HTML
        options = (cmarkgfmOptions.CMARK_OPT_UNSAFE)
        return cmarkgfm.github_flavored_markdown_to_html(processedMarkdown, options).strip()
