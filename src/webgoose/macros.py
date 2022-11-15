
from datetime import datetime
import time
import os

from src.webgoose.config import config
from src.webgoose.file_traverser import FileTraverser
from src.webgoose import version as webgoose_version

DATE_FORMAT = '%b %d %Y, %I:%M%p'


def last_modified(file_path, content, args):

    # TODO : MAKE WORK WITH BUILD PATH, CHECK IF MARKDOWN EXISTS IF BUILD DOESN'T (build may be new and later in to-build list)

    path = args['path'] if "path" in args else file_path

    date_format = args['format'] if "format" in args else DATE_FORMAT

    if os.path.exists(path):

        last_mod = datetime.fromtimestamp(os.path.getmtime(path))

        return last_mod.strftime(DATE_FORMAT)

    return ""





def get_version(filePath, content, args):
    return webgoose_version




def table_of_contents(filePath, content, args):
    return ""




def get_time(filePath, content, args):
    
    format = args['format'] if "format" in args else DATE_FORMAT

    return time.strftime(format)




def index(file_path, content, args):

    print(os.path.dirname(file_path))
    
    traverser = FileTraverser(os.path.dirname(file_path))

    _ , pages = traverser.find(".md")

    print(pages)

    index_list = list(map(lambda x: f"<li>{x}</li>", pages))

    if not "include_current" in args:

        index_list.remove(file_path)

    return f"<ul> {' '.join(index_list)} </ul>"



def docroot(filePath, content, args):
    return config['site']['doc-root']