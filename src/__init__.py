from flask import Flask
import os

project_root = os.path.dirname(os.path.dirname(__file__))
app = Flask(__name__, static_folder="../static", static_url_path="/static", template_folder="../template")

from src.route import primary_routes