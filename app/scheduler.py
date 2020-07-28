import os
from datetime import datetime
from hashlib import sha512
from requests import request

from dotenv import load_dotenv
from flask_apscheduler import APScheduler


load_dotenv()


def init_scheduler():
    scheduler = APScheduler()
    scheduler.add_job(
        func=change_webhook_url, trigger="interval", seconds=1500, id="12345"
    )
    scheduler.start()


def change_webhook_url():

    webhook_url_global = sha512(bytes(str(datetime.now()), "utf-8")).hexdigest()
    request(
        "get",
        "https://api.telegram.org/bot%s/setWebhook?url=https://masquerbot.herokuapp.com/webhook/%s"
        % (os.getenv("TELEGRAM_BOT_TOKKEN"), webhook_url_global),
    )
