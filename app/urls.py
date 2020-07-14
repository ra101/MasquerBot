from flask_restful import Api

from app.controllers import HomeController


api = Api()

api.add_resource(HomeController, "/home.html")
