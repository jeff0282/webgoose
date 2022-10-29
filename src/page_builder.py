
# PageBuilder
# ---
# The Heart Of WebGoose
#
# - Build Partial HTML From Markdown/HTML + YAML Metadata
# - Inserts Said HTML Into Templates And Outputs

import frontmatter, os, re, markdown, cmarkgfm
from src import project_root
from xml.dom import minidom
from flask import abort, render_template_string

class PageBuilder(object):

    def __init__(self, fullPath): 
        self.path = fullPath
        self.page = self.getPageFromFS()


    def getPageFromFS(self):

        with open(self.path) as file:
            page = frontmatter.load(file)

        return page


    def metaExists(self, key, expType):
        if key in self.page.metadata:
            if type(self.page.metadata[key]) == expType:
                return True

        return False


    def templateExists(self, template):
        templatePath = os.path.join(project_root, f"template/{template}")
        if os.path.exists(templatePath):
            return True
        else:
            return False


    def buildPage(self):
        head = self.buildPageHead()
        body = self.buildPageBody()
        return head + "\n" + body


    def render(self):
        template = self.page.metadata["template"] if "template" in self.page.metadata else "default.html"
        if self.templateExists(template):
            page = "{% extends '"+template+"' %}" + self.buildPage()
            return render_template_string(page, content=page)
        else: 
            abort(500)

    
    def buildPageHead(self):
        # Create Base For Partial HTML Document
        root = minidom.Document()

        # Create & Append <head>
        head = root.createElement("head")
        root.appendChild(head)

        # Shorter Metadata VarName for Convenience
        metadata = self.page.metadata

        # Add Title Tags & Info
        if self.metaExists("title", str):
            title = root.createElement("title")
            txt = root.createTextNode(metadata["title"])
            title.appendChild(txt)

            ogTitle = root.createElement("meta")
            ogTitle.setAttribute("property", "og:title")
            ogTitle.setAttribute("value", metadata["title"])

            head.appendChild(title)
            head.appendChild(ogTitle)
        else:
            abort(500)

        # Add Open Graph Description
        if self.metaExists("description", str):
            desc = root.createElement("meta")
            desc.setAttribute("property", "og:description")
            desc.setAttribute("value", metadata["description"])
            head.appendChild(desc)

        # Add Open Graph Image
        if self.metaExists("image", str):
            image = root.createElement("meta")
            image.setAttribute("property", "og:image")
            image.setAttribute("value", metadata["image"])
            head.appendChild(image)

        # Add Extra CSS 
        if self.metaExists("extra-css", list):
            for stylesheet in metadata['extra-css']:
                css = root.createElement("link")
                css.setAttribute("rel", "stylesheet")
                css.setAttribute("href", stylesheet)
                head.appendChild(css)

        if self.metaExists("extra-css", str):
            css = root.createElement("link")
            css.setAttribute("rel", "stylesheet")
            css.setAttribute("href", metadata["extra-css"])
            head.appendChild(css)

        # Make DOM Pretty (Add 4 Space Tab Indentations)
        # Remove <?xml ?> Tag, As This Is Only A Partial Segment
        finalDOM = root.toprettyxml(indent ="\t")
        finalDOM = re.sub("^<\?xml.*\?>", "", finalDOM) 
        
        return "{% block head %}" + finalDOM + "{% endblock %}"


    
    def buildPageBody(self):

        # Get Content Of Page, Convert Markdown to HTML
        # !!! SANITIZE !!!
        pageContent = cmarkgfm.github_flavored_markdown_to_html(self.page.content)

        # Add Div Around Page Content (XML IS ONLY VALID WITH A SINGLE ROOT)
        # parseString() will fail if this isn't done
        pageContent = f"<body>{pageContent.strip()}</body>"

        # Parse HTML Content And Append To Partial DOM
        pageContent = minidom.parseString(pageContent)

        # Make DOM Pretty (Add 4 Space Tab Indentations)
        # Remove <?xml ?> Tag, As This Is Only A Partial Segment
        finalDOM = pageContent.toprettyxml(indent ="\t")
        finalDOM = re.sub("^<\?xml.*\?>", "", finalDOM) 
        
        return "{% block body %}" + finalDOM + "{% endblock %}"










