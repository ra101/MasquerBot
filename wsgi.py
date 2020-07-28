from app import create_app
from app.scheduler import init_scheduler, change_webhook_url
from app.masquer_bot import bot

change_webhook_url()
init_scheduler()
application = create_app()
