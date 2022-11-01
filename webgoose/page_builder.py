
from bs4 import BeautifulSoup
from flask import render_template_string
from webgoose import project_root
import webgoose.util as util
import frontmatter, cmarkgfm, re, os


class PageBuilderException():
    
    def __init__(self):
        pass


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

        # Write New Build To File
        self.outputBuildToFile(newBuild)


    def renderPage(self, body):
        template = self.page.metadata["template"] if "template" in self.page.metadata else "default.html"
        if util.templateExists(template):
            pageContent = "{% extends '"+template+"' %}" + "{% block content %}" + body + "{% endblock %}"
            return render_template_string(pageContent, meta=self.page.metadata)
        else:
            raise PageBuilderException(f"Template {template} Does Not Exist")


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
        
    

    def createPageBody(self):
        return cmarkgfm.github_flavored_markdown_to_html(self.page.content).strip()


    def outputBuildToFile(self, pageBuild):
        if not os.path.exists(os.path.dirname(self.buildPath)):
            os.makedirs(os.path.dirname(self.buildPath))
        
        with open(self.buildPath, "w", encoding="utf-8") as file:
            file.write(pageBuild)


    def getPageContent(self):
        # Request_Handler Checks For Markdown File's Existence Beforehand
        with open(self.markdownPath, "r") as file:
            return frontmatter.load(file)




class PageBuilderException(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message