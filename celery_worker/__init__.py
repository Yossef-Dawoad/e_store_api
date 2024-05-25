import time

from celery import Celery

from e_store.config import get_settings

setting = get_settings()

celery = Celery(__name__)
celery.conf.brocker_url = setting.brocker_url
celery.conf.result_backend = setting.brocker_url


@celery.task(name="create_task")
def create_test_task(num1: float, num2: float) -> float:
    time.sleep(4)
    return num1 + num2
