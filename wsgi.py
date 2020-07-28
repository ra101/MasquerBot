from app import create_app
from app.scheduler import init_scheduler

init_scheduler()
application = create_app()
