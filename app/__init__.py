from flask import Flask
from flask_restful import Api

from app.models import db
from app.routes import APIs


def create_app():

    app = Flask(__name__)

    app.config.from_pyfile("config.py")
    db.init_app(app)
    APIs.init_app(app)

    return app
