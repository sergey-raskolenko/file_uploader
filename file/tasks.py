from celery import shared_task
from file.models import File
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task()
def file_treatment(file_id: int) -> None:
    file = File.objects.get(pk=file_id)
    file.processed = True
    file.save()
    logger.info(f"File {file} was treated")
