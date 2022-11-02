
import frontmatter, cmarkgfm, re, os, json, time
from bs4 import BeautifulSoup
from flask import render_template_string
from webgoose import project_root
from webgoose.macro_processor import MacroProcessor
from cmarkgfm.cmark import Options as cmarkgfmOptions

import importlib
util = importlib.import_module('webgoose.util')        


class PageBuilder(object):

    def __init__(self, markdownPath, buildPath, buildInfoPath):
        self.markdownPath = markdownPath
        self.buildPath = buildPath
        self.buildInfoPath = buildInfoPath
        self.page = self.getPageContent()


    def buildPage(self):
        # Generate Body Content
        body = self.createPageBody()

        # Use Body To Fill In Metadata Where Requires
        self.checkAddMetadata(body)

        # Render New Page Build
        newBuild = self.renderPage(body)

        # Create Build Info Document
        newBuildInfo = self.createBuildInfo()

        # Write New Build To File
        self.outputBuildFiles(newBuild, newBuildInfo)



    def renderPage(self, body):
        if util.templateExists(self.page.metadata['template']):
            pageContent = "{% extends '"+self.page.metadata['template']+"' %}" + "{% block content %}" + body + "{% endblock %}"
            renderedTemplate = render_template_string(pageContent, meta=self.page.metadata)
            htmlSoup = BeautifulSoup(renderedTemplate, "html.parser")
            return htmlSoup.prettify()
        else:
            raise PageBuilderException(f"Template {self.page.metadata['template']} Does Not Exist")



    def checkAddMetadata(self, body):
        htmlSoup = BeautifulSoup(body, "html.parser")

        if not "title" in self.page.metadata:
            self.page.metadata['title'] = htmlSoup.find(re.compile("^h[1-6]$")).string

        if not "title" in self.page.metadata:
            title = htmlSoup.find(re.compile("^h[1-6]$"))
            if title:
                self.page.metadata['title'] = title.string
            else: 
                self.page.metadata['title'] = "No Title"

        if not "description" in self.page.metadata:
            firstPara = htmlSoup.find("p")
            if firstPara:
                self.page.metadata['description'] = firstPara.string[:80]
            else: 
                self.page.metadata['description'] = "No Description Was Provided For This Page"

        if not "template" in self.page.metadata:
            self.page.metadata['template'] = "default.html"
        
    

    def createPageBody(self):
        # Process Macros 
        processor = MacroProcessor(self.page.content)
        processedMarkdown = processor.processMacros()

        # Convert Markdown To HTML
        options = (cmarkgfmOptions.CMARK_OPT_UNSAFE)
        return cmarkgfm.github_flavored_markdown_to_html(processedMarkdown, options).strip()



    def createBuildInfo(self):

        buildInfo = {
            "template": self.page.metadata['template']
        }

        return json.dumps(buildInfo, indent=4)



    def outputBuildFiles(self, pageBuild, buildInfo):
        if not os.path.exists(os.path.dirname(self.buildPath)):
            os.makedirs(os.path.dirname(self.buildPath))
        
        with open(self.buildPath, "w", encoding="utf-8") as file:
            file.write(pageBuild)

        with open(self.buildInfoPath, "w", encoding="utf-8") as file:
            file.write(buildInfo)



    def getPageContent(self):
        # Request_Handler Checks For Markdown File's Existence Beforehand
        with open(self.markdownPath, "r") as file:
            return frontmatter.load(file)




class PageBuilderException(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message