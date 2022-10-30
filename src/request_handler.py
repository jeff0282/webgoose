
# RequestHandler
# ---

from src.page_builder import PageBuilder
from src import project_root
from flask import abort
import os, time

class RequestHandler(object):

    def __init__(self, URI):
        self.URI = URI
        self.pagePath = self.getPagePath()
        self.buildPath = self.getBuildPath()


    def handle(self):
        if self.pageExists():
            if self.pageNeedsBuilt():
                print("serving new build")
                page = self.buildPage()
                return page
            else:
                print("serving existing build")
                return self.getPage()

        abort(404)


    def getPagePath(self):
        relPagePath = f"{self.URI}index.md" if self.URI[-1] == "/" else f"{self.URI}.md"
        return os.path.join(project_root, f"site/{relPagePath}")


    def getBuildPath(self):
        relBuildPath = f"{self.URI}index.html" if self.URI[-1] == "/" else f"{self.URI}.html"
        return os.path.join(project_root, f"build/{relBuildPath}")


    def pageExists(self):
        return os.path.exists(self.pagePath)


    def pageHasBuild(self):
        return os.path.exists(self.buildPath)


    def pageNeedsBuilt(self):
        if self.pageHasBuild():
            lastModTime = os.path.getmtime(self.pagePath) 
            lastBuildTime = os.path.getmtime(self.buildPath)
            return (lastModTime > lastBuildTime) | (time.time() - lastBuildTime > 86400)

        return True


    def buildPage(self):
        builder = PageBuilder(self.pagePath, self.buildPath)
        return builder.buildPage()


    def getPage(self):
        with open(self.buildPath) as page:
            pageContent = page.read()

        return pageContent