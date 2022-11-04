
import importlib, re, os, time
from webgoose import config
from webgoose.page_builder import PageBuilder
util = importlib.import_module('webgoose.util')


class BuildHandler(object):

    def __init__(self):
        pass


    def buildAll(self):
        for(searchDir, dirs, files) in os.walk(config['BUILD-OPTIONS']['source-dir'], topdown=True):
            for file in files:
                if file[-3:] == ".md": 
                    self.buildPage(os.path.join(searchDir, file))
                else:
                    pass
                    # LOG ERROR



    def buildPage(self, relativePath):
        markdownPath = os.path.abspath(relativePath)
        buildPath = util.getBuildPathFromRelPath(relativePath)

        lastModTime = os.path.getmtime(markdownPath)
        lastBuildTime = os.path.getmtime(buildPath)
        if lastModTime > lastBuildTime:
            print(f"Building: {relativePath}")
            builder = PageBuilder()
            fullPage = builder.buildPage(markdownPath)
            self.outputBuildToFile(buildPath, fullPage)
        
        return


    
    def outputBuildToFile(self, buildPath, pageBuild):

        if not os.path.exists(os.path.dirname(buildPath)):
            os.makedirs(os.path.dirname(buildPath))
        
        with open(buildPath, "w", encoding="utf-8") as file:
            file.write(pageBuild)

