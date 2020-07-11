from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

from app.config import SQLALCHEMY_DATABASE_URI

db = SQLAlchemy()

# engine = create_engine(SQLALCHEMY_DATABASE_URI)


# class User(db.Model):
#     __tablename__ = "Users"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(120), unique=True)
#     email = db.Column(db.String(120), unique=True)
#     password = db.Column(db.String(30))

#     def __init__(self, name=None, password=None):
#         self.name = name
#         self.password = password


# # Create tables.
# Base.metadata.create_all(bind=engine)
