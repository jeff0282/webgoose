
import re

def getFilenameFromPath(filePath):
    filePath = re.sub("\..+$", "", filePath)
    lastSlashIndex = filePath.rfind("/")
    if lastSlashIndex > 0:
        return filePath[lastSlashIndex+1:]
    else:
        return filePath
