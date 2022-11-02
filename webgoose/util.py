
from webgoose import project_root
from pathvalidate import is_valid_filepath
import os


# ======================
# URL AND PATH UTILS
# ======================

def validateURI(URI):
    if len(URI) > 1:
        if URI[0] == "/":
            URI = URI[1:]
        return is_valid_filepath(URI)
    else:
        return True


def getMarkdownPath(URI):
    relativePath = getPathFromProjectRoot(URI, "site", ".md")
    return getAbsolutePath(relativePath)


def getBuildPath(URI):
    relativePath = getPathFromProjectRoot(URI, "build", ".html")
    return getAbsolutePath(relativePath)


def getBuildInfoPath(URI):
    relativePath = getPathFromProjectRoot(URI, "build", ".json")
    return getAbsolutePath(relativePath)


def getPathFromProjectRoot(URI, pathFromProjectRoot, extension):
    path = URIToRelativePath(URI)
    relativePath = os.path.join(pathFromProjectRoot, path+extension)
    return relativePath


def getAbsolutePath(relativePath):
    absolutePath = os.path.join(project_root, relativePath)
    return absolutePath


def URIToRelativePath(URI):
    if len(URI) > 1:
        if URI[0] == "/": URI = URI[1:]
        return f"{URI}index" if URI[-1] == "/" else f"{URI}"
    else:
        return "index"



# ======================
# RESOURCE EXISTS UTILS
# ======================

def templateExists(relativeTemplatePath):
    return os.path.exists(os.path.join(project_root, f"template/{relativeTemplatePath}"))