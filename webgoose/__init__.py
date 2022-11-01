from flask import Flask
import os

project_root = os.path.dirname(os.path.dirname(__file__))
app = Flask(__name__, 
            static_url_path="/static", 
            static_folder=os.path.join(project_root, "static"), 
            template_folder=os.path.join(project_root, "template")
           )

# READ FROM CONFIG

from webgoose import routes

if __name__ == '__main__':
    app.run()