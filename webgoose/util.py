
from webgoose import project_root
import os


# ======================
# URL AND PATH UTILS
# ======================

def sanitizeURI(URI):
        # TODO
        return URI


def getMarkdownPath(URI):
    relativePath = getPathFromProjectRoot(URI, "site", ".md")
    print(relativePath)
    return getAbsolutePath(relativePath)


def getBuildPath(URI):
    relativePath = getPathFromProjectRoot(URI, "build", ".html")
    return getAbsolutePath(relativePath)


def getBuildInfoPath(URI):
    relativePath = getPathFromProjectRoot(URI, "build", ".json")
    return getAbsolutePath(relativePath)


def getPathFromProjectRoot(URI, pathFromProjectRoot, extension):
    path = expandURIShortening(URI)
    relativePath = os.path.join(project_root , f"{pathFromProjectRoot}/{path}{extension}")
    return relativePath


def getAbsolutePath(relativePath):
    absolutePath = os.path.join(project_root, relativePath)
    return absolutePath


def expandURIShortening(URI):
    if len(URI) > 1:
        return f"{URI}index" if URI[-1] == "/" else f"{URI}"
    else:
        return "index"



# ======================
# RESOURCE EXISTS UTILS
# ======================

def templateExists(relativeTemplatePath):
    return os.path.exists(os.path.join(project_root, f"template/{relativeTemplatePath}"))