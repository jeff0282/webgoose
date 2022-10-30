
# PageBuilder
# ---
# The Heart Of WebGoose
#
# - Build Partial HTML From Markdown/HTML + YAML Metadata
# - Inserts Said HTML Into Templates And Outputs

import frontmatter, os, re, markdown, cmarkgfm
from src import project_root
from xml.dom import minidom
from bs4 import BeautifulSoup
from flask import abort, render_template_string

class PageBuilder(object):

    def __init__(self, pagePath, buildPath): 
        self.pagePath = pagePath
        self.buildPath = buildPath
        self.page = self.getPageInfo()
        


    def getPageInfo(self):

        with open(self.pagePath) as file:
            page = frontmatter.load(file)

        return page



    def metaExists(self, key, expType, silent=True):
        if key in self.page.metadata:
            if type(self.page.metadata[key]) == expType:
                return True
            
        if silent:
            # THROW EXCEPTION
            return False
        else:
            return False



    def templateExists(self, template):
        templatePath = os.path.join(project_root, f"template/{template}")
        return os.path.exists(templatePath)



    def buildPage(self):
        # Validate Page Metadata - Throw Exception If Invalid
        if not self.validateMetadata():
            # THROW EXCEPTION
            abort(500)

        # Generate Content of Page, Decide On Template To Use, Add Jinja2 Template Inheritance Stuff
        template = self.page.metadata["template"] if "template" in self.page.metadata else "default.html"
        body = "{% extends '"+template+"' %}" + self.generatePageContent()
        
        # Build Page Using Jinja2 (Flask), Prettify HTML (correct indentation, etc), Update Current Build
        renderedPage = render_template_string(body, meta=self.page.metadata)
        soup = BeautifulSoup(renderedPage, "html.parser")
        renderedPage = str(soup.prettify())
        print(renderedPage)
        self.writeBuildToFile(renderedPage)

        # Return Built Page For Display
        return renderedPage



    def validateMetadata(self):
        if not "title" in self.page.metadata:
            return False

        if "template" in self.page.metadata:
            if not self.templateExists(self.page.metadata['template']):
                return False

        typeCheck = list(map(lambda x: type(x) == str, self.page.metadata))
        if False in typeCheck:
            return False

        return True



    def writeBuildToFile(self, pageBuild):
        if not os.path.exists(os.path.dirname(self.buildPath)):
            os.makedirs(os.path.dirname(self.buildPath))
        
        with open(self.buildPath, "w", encoding="utf-8") as file:
            file.write(pageBuild)



    """
    def createXMLTag(self, tagName, **kwargs):

        tag = f"<{tagName}"

        if "attr" in kwargs:
            attributes = " "
            for k, v in kwargs["attr"].items():
                attributes += f"{k}='{v}' "
            tag += attributes

        if "text" in kwargs:
            return f"{tag}>{kwargs['text']}</{tagName}>\n"
        
        return f"{tag.strip()}/>\n"

    

    def buildPageHead(self):

        head = ""

        # Shorter Metadata VarName for Convenience
        meta = self.page.metadata

        # Add Title Tags & Info
        if self.metaExists("title", str):
            head += self.createXMLTag("title", text=meta['title'])
            head += self.createXMLTag("meta", attr={"property": "og:title", "value": meta['title']})
        else:
            abort(500)

        # Add Open Graph Description
        if self.metaExists("description", str):
            head += self.createXMLTag("meta", attr={"property": "og:description", "value": meta['description']})

        # Add Open Graph Image
        if self.metaExists("image", str):
            head += self.createXMLTag("meta", attr={"property": "og:image", "value": meta['image']})

        # Add Extra CSS 
        if self.metaExists("extra-css", list):
            for stylesheet in metadata['extra-css']:
                head += self.createXMLTag("link", attr={"rel": "stylesheet", "href": stylesheet})

        if self.metaExists("extra-css", str):
            head += self.createXMLTag("link", attr={"rel": "stylesheet", "href": meta['extra-css']})
        
        return "{% block head %}" + head + "{% endblock %}"
    """

    def generatePageContent(self):
        # Get Content Of Page, Convert Markdown to HTML
        pageContent = cmarkgfm.github_flavored_markdown_to_html(self.page.content)
        pageContent = f"{pageContent.strip()}"
        
        return "{% block body %}" + pageContent + "{% endblock %}"










