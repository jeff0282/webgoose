
import os, datetime
from src.webgoose.config import config

DATE_FORMAT = '%b %d %Y, %I:%M %p'


def last_modified(file_path, content, args):
    if len(args) > 0:
        if os.path.exists(args[0]):
            date = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            return date.strftime(DATE_FORMAT)
        else: 
            return ""
    
    date = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
    return date.strftime(DATE_FORMAT)


def version(filePath, content, args):
    return "In Development"


def table_of_contents(filePath, content, args):
    return ""


def random(filePath, content, args):
    print(args)
    return "my balls lol"


def time(filePath, content, args):
    return ""

def index(file_path, content, args):
    pass

def docroot(filePath, content, args):
    return config['SITE-OPTIONS']['doc-root']