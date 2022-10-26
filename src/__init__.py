from flask import Flask

app = Flask(__name__, static_folder="../static", static_url_path="/static", template_folder="../template")

from src.route import primary