'''
./app/routes.py
'''
from flask_restful import Api

from app.controllers import HomeController, WebhookController, FaviconController


def init_routes(app):
    APIs = Api(app)
    APIs.add_resource(HomeController, "/home.html")
    APIs.add_resource(FaviconController, "/favicon.ico")
    APIs.add_resource(WebhookController, "/<webhook_url>/webhook")
