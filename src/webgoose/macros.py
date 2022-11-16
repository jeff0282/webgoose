
import os
import time
from datetime import datetime

from src.webgoose import version as webgoose_version
from src.webgoose.config import config
from src.webgoose.file_traverser import FileTraverser



DATE_FORMAT = '%b %d %Y, %I:%M%p'



def last_modified(page_dict, content, args):

    path = page_dict['build_path']

    date_format = args['format'] if "format" in args else DATE_FORMAT

    # Return Last Build Time If Available
    # Otherwise, return current time (assume page source exists but later in build queue)
    if os.path.exists(path):

        last_mod = datetime.fromtimestamp(os.path.getmtime(path))

        return last_mod.strftime(DATE_FORMAT)

    
    return time.time()






def get_version(page_dict, content, args):
    return webgoose_version




def table_of_contents(page_dict, content, args):
    return ""




def get_time(page_dict, content, args):
    
    format = args['format'] if "format" in args else DATE_FORMAT

    return time.strftime(format)




def index(page_dict, content, args):

    traverser = FileTraverser(os.path.dirname(page_dict['source_path']))

    _ , pages = traverser.find(".md")

    if not "include_current" in args:

        pages.remove(page_dict['filename'])


    index_list = list(map(lambda x: f"<li>{x}</li>", pages))

    return f"<ul> {''.join(index_list)} </ul>"



def docroot(page_dict, content, args):
    return os.path.join(config['site']['doc-root'], config['build']['build-dir'])