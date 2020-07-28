import os

import telegram
from dotenv import load_dotenv
from flask_restful import Resource


from app.models import db  # , User
from app.masquer_bot import bot, dp, update_queue, get_updates


class HomeController(Resource):
    def get(self):
        return "Hello World"


class WebhookController(Resource):
    def post(self, webhook_url):

        update = get_updates()
        chat_id = update.message.chat.id
        msg_id = update.message.message_id

        with open("webhook_url", "r") as f:
            temp = f.read()

        if webhook_url == temp:
            dp.process_update(update)
            update_queue.put(update)

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

        return "OK"
