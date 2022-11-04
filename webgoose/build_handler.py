
import importlib, re, os
from webgoose.page_builder import PageBuilder
#util = importlib.import_module('webgoose.util')


class BuildHandler(object):

    MARKDOWN_DIR = "src"
    BUILD_DIR = "build"


    def __init__(self):
        pass



    def buildAll(self):
        for(searchDir, dirs, files) in os.walk(self.MARKDOWN_DIR, topdown=True):
            for file in files:
                if file[-3:] == ".md": 
                    self.buildPage(os.path.join(searchDir, file))
                else:
                    pass
                    # LOG ERROR



    def buildPage(self, relativePath):
        absolutePath = os.path.abspath(relativePath)
        builder = PageBuilder()
        fullPage = builder.buildPage(absolutePath)
        self.outputBuildToFile(relativePath, fullPage)
        return fullPage



    
    def outputBuildToFile(self, relativePath, pageBuild):

        buildPath = re.sub(f"^{self.MARKDOWN_DIR}\/", f"{self.BUILD_DIR}/", relativePath)
        buildPath = re.sub(r"\.md$", ".html", buildPath)
        absolutePath = os.path.abspath(buildPath)

        if not os.path.exists(os.path.dirname(absolutePath)):
            os.makedirs(os.path.dirname(absolutePath))
        
        with open(absolutePath, "w", encoding="utf-8") as file:
            file.write(pageBuild)

