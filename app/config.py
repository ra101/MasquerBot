import os

from dotenv import load_dotenv


load_dotenv()

DEBUG = True if os.getenv("FLASK_DEBUG") == "True" else False
SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
ENV = os.getenv("FLASK_ENV")

SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = (
    True if os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS") == "True" else False
)
