
from webgoose.page_builder import PageBuilder
from webgoose import project_root
import webgoose.util as util
from flask import abort
import time, os


class PageNotFoundException(Exception):

    def __init__(self, URI):
        self.URI = URI

    def __str__(self):
        return f"[RequestHandler - PageNotFoundException] The Page At URI '{self.URI}' Was Not Found"


class RequestHandler(object):

    def __init__(self, URI, buildHandler=PageBuilder):
        self.time = time.time()
        self.handler = buildHandler
        self.URI = util.sanitizeURI(URI)
        self.markdownPath = util.getMarkdownPath(self.URI)
        self.buildPath = util.getBuildPath(self.URI)
        self.buildInfoPath = util.getBuildInfoPath(self.URI)


    def handleRequest(self):
        try:
            if os.path.exists(self.markdownPath):
                if self.requiresRebuild():
                    builder = self.handler(self.markdownPath, self.buildPath, self.buildInfoPath)
                    builder.buildPage()

                return self.getCurrentBuild()
            else:
                raise PageNotFoundException(self.URI)

        except PageNotFoundException as e:
            print(e)
            abort(404)

        except Exception as e:
            print(e)
            abort(500)


    def requiresRebuild(self):
        if os.path.exists(self.buildPath):
            buildTime = os.path.getmtime(self.buildPath)
            lastModTime = os.path.getmtime(self.markdownPath)
            return (lastModTime > buildTime)

        return True


    def getCurrentBuild(self):
        with open(self.buildPath, "r") as file:
            return(file.read())
