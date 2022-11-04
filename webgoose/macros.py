
import os, importlib, datetime
util = importlib.import_module("webgoose.util")

DATE_FORMAT = '%b %d %Y, %I:%M %p'

def created(markdownPath, content, args):
    if len(args) > 0:
        if os.path.exists(args[0]):
            markdownPath = util.getMarkdownPath(args[0])
            date = datetime.datetime.fromtimestamp(os.path.getctime(markdownPath))
            return date.strftime(DATE_FORMAT)
        else: 
            return ""
    
    date = datetime.datetime.fromtimestamp(os.path.getctime(markdownPath))
    return date.strftime(DATE_FORMAT)


def lastModified(markdownPath, content, args):
    if len(args) > 0:
        if os.path.exists(args[0]):
            markdownPath = util.getMarkdownPath(args[0])
            date = datetime.datetime.fromtimestamp(os.path.getmtime(markdownPath))
            return date.strftime(DATE_FORMAT)
        else: 
            return ""
    
    date = datetime.datetime.fromtimestamp(os.path.getmtime(markdownPath))
    return date.strftime(DATE_FORMAT)


def version(markdownPath, content, args):
    return "In Development"


def tableOfContents(markdownPath, content, args):
    return ""


def random(markdownPath, content, args):
    return ""


def builtUsing(markdownPath, content, args):
    return ""