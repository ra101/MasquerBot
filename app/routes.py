from flask_restful import Api

from app.controllers import HomeController, WebhookController


APIs = Api()

APIs.add_resource(HomeController, "/home.html")
APIs.add_resource(WebhookController, "/webhook")
