
from src.request_handler import RequestHandler
from src import app

@app.route('/')
def index_route():
    return page_route("/")

@app.route('/<path:pagePath>')
def page_route(pagePath):
    handler = RequestHandler(pagePath)
    return handler.handle()