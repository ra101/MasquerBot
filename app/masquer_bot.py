import os
from hashlib import sha512

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
    try:
        db.session.commit()
        bot.send_message(message.chat.id, account.public_key)
    except:
        pass


@bot.message_handler(commands=["get_key"])
def get_key(message):
    username = message.from_user.username
    try:
        bot.send_message(
            message.chat.id,
            UserAccount.query.filter_by(
                username_hash=sha512(bytes(username, "utf-8")).hexdigest()
            )
            .first()
            .public_key,
        )
    except:
        bot.reply_to(message, "Unable to fetch userkey.")


@bot.message_handler(commands=["help"])
def help(message):
    bot.reply_to(message, "Yo! help arrived!")


@bot.message_handler(func=lambda message: True, content_types=["text"])
def echo_message(message):
    bot.reply_to(message, message.text)
