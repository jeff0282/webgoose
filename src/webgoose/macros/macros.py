
import os, importlib, datetime
from webgoose import config
util = importlib.import_module("webgoose.util")

DATE_FORMAT = '%b %d %Y, %I:%M %p'


def lastModified(filePath, content, args):
    if len(args) > 0:
        if os.path.exists(args[0]):
            filePath = util.getfilePath(args[0])
            date = datetime.datetime.fromtimestamp(os.path.getmtime(filePath))
            return date.strftime(DATE_FORMAT)
        else: 
            return ""
    
    date = datetime.datetime.fromtimestamp(os.path.getmtime(filePath))
    return date.strftime(DATE_FORMAT)


def version(filePath, content, args):
    return "In Development"


def tableOfContents(filePath, content, args):
    return ""


def random(filePath, content, args):
    return ""


def builtUsing(filePath, content, args):
    return ""

def docroot(filePath, content, args):
    return config['SITE-OPTIONS']['doc-root']