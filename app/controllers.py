import os

from telebot.types import Update
from dotenv import load_dotenv
from flask_restful import Resource
from flask import request

from app.masquer_bot import bot


class HomeController(Resource):
    def get(self):
        return "Hello World"


class WebhookController(Resource):
    def post(self, webhook_url):

        with open("webhook_url", "r") as f:
            temp = f.read()

        if webhook_url == temp:
            bot.process_new_updates(
                [Update.de_json(request.stream.read().decode("utf-8"))]
            )
        return "!", 200
