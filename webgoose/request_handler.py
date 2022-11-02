
from webgoose.page_builder import PageBuilder
from webgoose import project_root
from flask import abort
import os

import importlib
util = importlib.import_module('webgoose.util')


class PageNotFoundException(Exception):
    def __init__(self, URI):
        self.URI = URI
        self.message = "The Page Was Not Found"

    def __str__(self):
        return f"PageNotFoundException: ({self.URI}) {self.message}"


class RequestHandler(object):

    def __init__(self, URI, buildHandler=PageBuilder):
        
        # Check URI Before Proceeding, Terminate If Sus
        if util.validateURI(URI):
            self.URI = URI
        else:
            abort(404)

        self.buildHandler = buildHandler
        self.markdownPath = util.getMarkdownPath(self.URI)
        self.buildPath = util.getBuildPath(self.URI)
        self.buildInfoPath = util.getBuildInfoPath(self.URI)


    def handleRequest(self):
        #try:
        if os.path.exists(self.markdownPath):
            if self.requiresRebuild():
                builder = self.buildHandler(self.markdownPath, self.buildPath, self.buildInfoPath)
                builder.buildPage()

            return self.getCurrentBuild()
        else:
            pass
            #raise PageNotFoundException(self.URI)

        #except PageNotFoundException as e:
            
            #abort(404)

        #except Exception as e:
            #abort(500)


    def requiresRebuild(self):
        """
        if os.path.exists(self.buildPath):
            buildTime = os.path.getmtime(self.buildPath)
            lastModTime = os.path.getmtime(self.markdownPath)
            return (lastModTime > buildTime)
        """

        return True


    def getCurrentBuild(self):
        with open(self.buildPath, "r") as file:
            return(file.read())
