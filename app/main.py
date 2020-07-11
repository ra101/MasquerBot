from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.models import db

app = Flask(__name__)
app.config.from_object("app.config")
db.init_app(app)


@app.teardown_request
def shutdown_session(exception=None):
    db.session.remove()


@app.route("/home.html")
def hello_world():
    return "Hello World"


# def my_function():
#     with app.app_context():
#         user = db.User(...)
#         db.session.add(user)
#         db.session.commit()
