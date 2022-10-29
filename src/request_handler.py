
# RequestHandler
# ---

from src.page_builder import PageBuilder
from src import project_root
from flask import abort
import os

class RequestHandler(object):

    def __init__(self, URI):
        self.URI = URI

    def loadPage(self):
        pagePath = os.path.join(project_root, f"site/{self.URI}")
        if pagePath[-1] == "/":
            pagePath += "index"
        pagePath += ".md"

        if os.path.exists(pagePath):
            builder = PageBuilder(pagePath)
            return builder.render()
        else:
            abort(404)