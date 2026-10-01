from celery import shared_task
from minio import Minio, S3Error
from services.catalog.config import settings
from services.catalog.celery import app

client = Minio(
    settings.MINIO_ENDPOINT.replace("http://", ""),
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False,
    region="us-east-1"  # MinIO требует регион для некоторых операций
)

@shared_task(bind=True, max_retries=3)
def remove_object(self, bucket, object_name):
    try:
        client.remove_object(bucket, object_name)
        return f"{object_name} is successfully deleted"
    except S3Error as e:
        self.retry(exc=e, countdown=5)


def enqueue_remove_object(bucket: str, object_name: str):
    """Отправка таска через send_task с producer=None (работает надежно)."""
    return app.send_task(
        "services.catalog.tasks.remove_object",
        args=[bucket, object_name],
        producer=None
    )
