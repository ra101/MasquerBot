'''
./app/__init__.py
'''
from flask import Flask

from app.models import db
from app.routes import init_routes


def create_app():

    app = Flask(__name__)

    app.config.from_pyfile("config.py")
    db.init_app(app)

    # Flask-RESTful init
    init_routes(app)

    # For db commits
    app.app_context().push()
    db.create_all()

    return app
