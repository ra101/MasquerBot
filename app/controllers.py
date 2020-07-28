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
    def post(self):
        update = telegram.Update.de_json(request.get_json(force=True), bot)

        chat_id = update.message.chat.id
        msg_id = update.message.message_id

        text = update.message.text.encode("utf-8").decode()
        print("got text message :", text)
        response = "response"
        bot.sendMessage(chat_id=chat_id, text=response, reply_to_message_id=msg_id)
        return "ok"
