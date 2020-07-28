'''
./app/controllers.py
'''
from telebot.types import Update
from flask_restful import Resource
from flask import request, redirect


from app.masquer_bot import bot


class HomeController(Resource):
    '''
    Unnecessary route, used for my pinger project [https://github.com/ra101/pinger]
    '''

    def get(self):
        return "Hello World"


class FaviconController(Resource):
    '''
    Unnecessary route, added without any reason.
    '''

    def get(self):
        return redirect(
            "https://raw.githubusercontent.com/ra101/MasquerBot/core/assets/favicon.ico"
        )


class WebhookController(Resource):
    def post(self, webhook_url):

        # opens the file for dynamic url
        with open("webhook_url", "r") as f:
            temp = f.read()

        if webhook_url == temp:
            bot.process_new_updates(
                [Update.de_json(request.stream.read().decode("utf-8"))]
            )
        return "!", 200
