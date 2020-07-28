import os
from queue import Queue

import telegram
from telegram.ext import Dispatcher
from dotenv import load_dotenv
from flask import request


load_dotenv()

# init Bot

global bot
global TOKEN
telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKKEN")
bot = telegram.Bot(token=telegram_bot_token)


update_queue = Queue()

dp = Dispatcher(bot, update_queue)


def get_updates():
    return telegram.Update.de_json(request.get_json(force=True), bot)
