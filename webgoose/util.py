
import re, os
from webgoose import config


def getFilenameFromPath(filePath):
    filePath = re.sub("\..+$", "", filePath)
    lastSlashIndex = filePath.rfind("/")
    if lastSlashIndex > 0:
        return filePath[lastSlashIndex+1:]
    else:
        return filePath


def getBuildPathFromRelPath(relativePath):
    buildPath = re.sub(f"^{config['BUILD-OPTIONS']['source-dir']}\/", f"{config['BUILD-OPTIONS']['build-dir']}/", relativePath)
    buildPath = re.sub(r"\.md$", ".html", buildPath)
    return os.path.abspath(buildPath)