import os
from re import fullmatch
from hashlib import sha512

import telebot
from dotenv import load_dotenv

from app.utils import decode_hex
from app.models import db, UserAccount, EncryptionCache

load_dotenv()

# init Bot

telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKKEN")

bot = telebot.TeleBot(telegram_bot_token, threaded=False)

re = compile


@bot.message_handler(commands=["start", "s"])
def start(message):
    username = message.from_user.username
    account = UserAccount(username)
    db.session.add(account)
    try:
        db.session.commit()
        bot.send_message(message.chat.id, str(account.public_key))
    except:
        db.session.rollback()
        pass


@bot.message_handler(commands=["get_key", "gh"])
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


@bot.message_handler(commands=["help", "h"])
def help(message):
    bot.send_message(message.chat.id, "Yo! help arrived!")


@bot.message_handler(commands=["encrypt", "e"])
def encrypt(message):
    db.session.add(EncryptionCache(message.chat.id))
    try:
        db.session.commit()
        bot.send_message(message.chat.id, "start encryption")
    except:
        db.session.rollback()
        bot.send_message(message.chat.id, "Cancel the ongoing event first.")


@bot.message_handler(func=lambda message: True, content_types=["text"])
def text_reply(message):
    try:
        cache = EncryptionCache.query.filter_by(chat_id=message.chat.id).first()
        if cache.message is None:
            cache.message = message.text
            try:
                db.session.commit()
                bot.send_message(message.chat.id, "Now send the recepient's public key")
            except:
                db.session.rollback()
                pass
        else:
            if (fullmatch("[0][xX][0-9a-fA-F]+", message.text) is not None) and (
                len(message.text) == 130
            ):
                cache.public_key = message.text
                try:
                    db.session.commit()
                    bot.send_message(message.chat.id, "Now send the Image")
                except:
                    db.session.rollback()
            else:
                bot.send_message(message.chat.id, "Invalid Key!, Send Again.")

    except:
        pass


@bot.message_handler(commands=["delete"])
def encrypt(message):
    EncryptionCache.query().delete()
    UserAccount.query().delete()
    try:
        db.session.commit()
    except:
        db.session.rollback()
