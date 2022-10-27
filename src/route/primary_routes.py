from flask import render_template_string, abort
from src import app, project_root
import frontmatter
import os

@app.route('/')
def index_route():
    return page_route('/')


@app.route('/pages/<path:pagePath>')
def page_route(pagePath):

    # DOING PROCEDURALLY FOR TESTING PURPOSES !!

    if pagePath[-1] == "/":
        pagePath += "index"

    pagePath = os.path.join(project_root, 'pages'+pagePath+'.md')
    with open(pagePath) as file:
        rawPage = frontmatter.load(file)
        print(rawPage)

    pageHead = buildPageHead(rawPage.metadata)
    return render_template_string(pageHead, content=pageHead)



# INAPPROPRIATELY PLACED FUNCTIONS, MOVE WHEN REFACTORING
# [LOOK INTO .format()]

def buildPageHead(metadata):
    
    # Check For Necessary Metadata
    if not "title" in metadata:
        return abort(500)

    pageHead = "<title>"+metadata["title"]+"</title>"
    pageHead += "<meta property='og:title' value='"+metadata["title"]+"'>"

    if "description" in metadata:
        pageHead += "<meta property='og:description' value='"+metadata["description"]+"'>"

    if "embed-img" in metadata:
        pageHead += "<meta property='og:image' value='"+metadata["embed-img"]+"'>"
    
    if "extra-css" in metadata:
        if type(metadata["extra-css"]) == list:
            for stylesheet in metadata["extra-css"]:
                pageHead += f"<link rel='stylesheet' href='{stylesheet}'>"
        elif type(metadata["extra-css"]) == str:
            pageHead += "<link rel='stylesheet' href='"+metadata["extra-css"]+"'>"
        else:
            abort(500)

    template = "default.html"
    if "custom-template" in metadata:
        templatePath = os.path.join(project_root, "template/"+metadata['custom-template'])
        print(templatePath)
        if os.path.exists(templatePath):
            template = metadata["custom-template"]
        else:
            abort(500)
    
    return "{% extends '"+template+"'%} {% block head_extra %}" + pageHead + "{% endblock %}"