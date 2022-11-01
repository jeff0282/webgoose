
from webgoose.request_handler import RequestHandler
from werkzeug.exceptions import HTTPException
from flask import redirect, render_template
from webgoose import app

# Serve Index Page
@app.route('/')
def index_route():
    return pageRoute("/")



# Serve Paths Other Than Index
@app.route('/<path:pagePath>')
def pageRoute(pagePath):
    handler = RequestHandler(pagePath)
    return handler.handleRequest()



# Error Handling Routes
@app.errorhandler(404)
def notFoundRoute(e):
    return render_template("site-essential/error-404.html")

@app.errorhandler(500)
def generalException(e):
    return render_template("site-essential/error-500.html")



# Special Case Routes
# -------------------
# Redirect requests for favicon to the static folder
@app.route("/favicon.ico")
def faviconRedirect():
    return redirect("/static/favicon.ico")