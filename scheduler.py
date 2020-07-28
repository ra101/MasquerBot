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

    webhook_url_global = sha512(bytes(str(datetime.now()), "utf-8")).hexdigest()
    request(
        "get",
        "https://api.telegram.org/bot%s/setWebhook?url=%s/%s/webhook"
        % (os.getenv("TELEGRAM_BOT_TOKKEN"), os.getenv("DOMAIN"), webhook_url_global,),
    )
    with open("webhook_url", "w") as f:
        f.write(webhook_url_global)


def on_starting(server):
    change_webhook_url()
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(func=change_webhook_url, trigger="interval", seconds=600)
    scheduler.start()
