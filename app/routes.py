from flask_restful import Api

from app.controllers import HomeController


APIs = Api()

APIs.add_resource(HomeController, "/home.html")
