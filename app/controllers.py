from flask_restful import Resource

from app.models import db, #User


class HomeController(Resource):
    def get(self):
        return "Hello World"
