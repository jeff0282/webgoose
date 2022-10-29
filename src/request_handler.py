
# RequestHandler
# ---

from src.page_builder import PageBuilder
from src import project_root
from flask import abort
import os, time

class RequestHandler(object):

    def __init__(self, URI):
        self.URI = f"{URI}index.md" if URI[-1] == "/" else f"{URI}.md"
        self.fullPath = self.getPagePath()
        self.buildPath = self.getBuildPath()


    def handle(self):
        if self.pageExists():
            if self.pageNeedsBuilt():
                page = self.buildPage()
                if not os.path.exists(os.path.dirname(self.buildPath)):
                    os.makedirs(os.path.dirname(self.buildPath))
                buildPage = open(self.buildPath, "w")
                buildPage.write(page)
                buildPage.close()
                return page
            else:
                return self.getPage()

        abort(404)


    def getPagePath(self):
        return os.path.join(project_root, f"site/{self.URI}")


    def getBuildPath(self):
        return os.path.join(project_root, f"build/{self.URI}")


    def pageExists(self):
        return os.path.exists(self.fullPath)


    def pageHasBuild(self):
        return os.path.exists(self.buildPath)


    def pageNeedsBuilt(self):
        if self.pageHasBuild():
            lastModTime = os.path.getmtime(self.fullPath) 
            lastBuildTime = os.path.getmtime(self.buildPath)
            print((lastModTime > lastBuildTime) | (time.time() - lastBuildTime > 86400))
            return (lastModTime > lastBuildTime) | (time.time() - lastBuildTime > 86400)

        return True



    def buildPage(self):
        builder = PageBuilder(self.fullPath)
        return builder.render()


    def getPage(self):
        with open(self.buildPath) as page:
            pageContent = page.read()

        return pageContent