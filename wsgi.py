from app import create_app
from app.scheduler import init_scheduler

global webhook_url_global
init_scheduler()
application = create_app()
