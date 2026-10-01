from celery import Celery
from services.catalog.config import settings

app = Celery("catalog")
app.conf.broker_url = settings.rabbitmq_url
app.conf.broker_pool_limit = 0  # отключаем пул, чтобы избежать проблем с connection pool
app.conf.timezone = "UTC"
app.conf.enable_utc = True

# Устанавливаем как default ДО импорта tasks, чтобы shared_task нашло current_app
app.set_default()

import services.catalog.tasks  # noqa: F401
