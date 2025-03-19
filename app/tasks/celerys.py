# from celery import Celery
# from app.config import settings
#
#
# celery = Celery(
#     "tasks",
#     broker=f"redis://{settings.redis_host}:{settings.redis_port}",
#     include=["app.tasks.tasks"]
# )
#
# celery.conf.update(
#     broker_connection_retry_on_startup=True  # Включает повторные попытки подключения при старте
# )