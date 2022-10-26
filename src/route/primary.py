from flask import render_template
from src import app

@app.route('/')
def index_route():
    return render_template("default.html")