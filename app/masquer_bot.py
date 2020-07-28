import os

import telebot
from dotenv import load_dotenv

from app.utils import decode_hex
from app.models import db, UserAccount

load_dotenv()

# init Bot

telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKKEN")

bot = telebot.TeleBot(telegram_bot_token, threaded=False)


@bot.message_handler(commands=["start"])
def start(message):
    username = message.from_user.username
    account = UserAccount(username)
    db.session.add(account)
    db.session.commit()
    bot.reply_to(message, account.public_key)


@bot.message_handler(commands=["help"])
def start(message):
    bot.reply_to(message, "Yo! help arrived!")


@bot.message_handler(func=lambda message: True, content_types=["text"])
def echo_message(message):
    bot.reply_to(message, message.text)
