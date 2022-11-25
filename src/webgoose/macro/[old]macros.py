
import os
import time
from datetime import datetime

from src.webgoose import version as webgoose_version
from src.webgoose.config import config
from src.webgoose.file_traverser import FileTraverser

DATE_FORMAT = '%b %d %Y, %I:%M%p'



def last_modified(page, content, args):

    date_format = args['format'] if "format" in args else DATE_FORMAT

    # Return Last Build Time If Available
    # Otherwise, return current time (assume page source exists but later in build queue)
    if os.path.exists(page.build_path):

        last_mod = datetime.fromtimestamp(os.path.getmtime(page.build_path))

        return last_mod.strftime(DATE_FORMAT)

    
    return time.strftime(DATE_FORMAT, time.localtime())






def get_version(page, content, args):
    return webgoose_version




def table_of_contents(page, content, args):
    return ""




def index(page, content, args):

    search_dir = os.path.dirname(page.source_path)

    traverser = FileTraverser(search_dir)

    _ , pages = traverser.find(".md")


    index_list = list(map(lambda x: f"<li>{x}</li>", pages))

    return f"<ul> {''.join(index_list)} </ul>"



def docroot(page, content, args):

    return config['site']['doc-root']