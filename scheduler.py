"""
./scheduler.py

This file is reponsible for dynamically chainging webhook url of bot. An added security layer.
Though it is named as scheduler.py but this is loaded as config file for gunicorn,
because of on_starting function.
Here APScheduler is used instead of Flask-APSheduler as flaskapp is not yet associacted with gunicorn.
"""
import os
from datetime import datetime
from hashlib import sha512
from requests import request

from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler


load_dotenv()


def init_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=change_webhook_url, trigger="interval", seconds=10, id="12345"
    )
    return scheduler


def change_webhook_url():
    """
    There is probably a way to create webhook in pyTelegramBotAPI but we will use requests,
    as bot is not loaded yet.
    """
    webhook_url_global = sha512(bytes(str(datetime.now()), "utf-8")).hexdigest()
    request(
        "get",
        "https://api.telegram.org/bot%s/setWebhook?url=%s/%s/webhook"
        % (
            os.getenv("TELEGRAM_BOT_TOKKEN"),
            os.getenv("DOMAIN_NAME"),
            webhook_url_global,
        ),
    )

    # File is used instead of env_variable 'cuz i could not get it working in heroku. if you can
    # feel free to send a PR
    with open("webhook_url", "w") as f:
        f.write(webhook_url_global)


# this function is loaded before fork is done by gunicorn
def on_starting(server):
    """
    After waking up from hibernation (heroku), first the webhook is is created then sheduler is started
    21900 -> 6 hours and 5 minutes.
    """
    change_webhook_url()
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(func=change_webhook_url, trigger="interval", seconds=21900)
    scheduler.start()
