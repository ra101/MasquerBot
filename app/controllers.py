import os

import telegram
from dotenv import load_dotenv
from flask import request
from flask_restful import Resource

from app.models import db  # , User


load_dotenv()
# init Bot
global bot
global TOKEN
TOKEN = os.getenv("TELEGRAM_BOT_TOKKEN")
bot = telegram.Bot(token=TOKEN)


class HomeController(Resource):
    def get(self):
        return "Hello World"


class WebhookController(Resource):
    def post(self, webhook_url):

        update = telegram.Update.de_json(request.get_json(force=True), bot)
        chat_id = update.message.chat.id
        msg_id = update.message.message_id

        if webhook_url == os.getenv("WEBHOOK_URL"):

            print(update)
            print(dir(update))
            print(update.message)
            print(dir(update.message))

            text = update.message.text.encode("utf-8").decode()

            response = "Yo!"
            if text == "/start":
                response = "Yo! I started"
            if text == "/help":
                response = "Yo! help arrived!"
            bot.sendMessage(chat_id=chat_id, text=response)
        else:
            bot.sendMessage(
                chat_id=chat_id, text="Please Send again.", reply_to_message_id=msg_id
            )
