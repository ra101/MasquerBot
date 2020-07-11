import os

from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True if os.getenv("FLASK_DEBUG") == "True" else False
SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, os.getenv("DB_NAME"))
SQLALCHEMY_TRACK_MODIFICATIONS = True if os.getenv("FLASK_DEBUG") == "True" else False
