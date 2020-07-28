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
        func=change_webhook_url, trigger="interval", seconds=10800, id="12345"
    )
    scheduler.start()


def change_webhook_url():

    webhook_url_global = sha512(bytes(str(datetime.now()), "utf-8")).hexdigest()
    request(
        "get",
        "https://api.telegram.org/bot%s/setWebhook?url=%s/%s"
        % (
            os.getenv("TELEGRAM_BOT_TOKKEN"),
            os.getenv("WEBHOOK_URL"),
            webhook_url_global,
        ),
    )

    with open("webhook_url", "w") as f:
        f.write(webhook_url_global)
