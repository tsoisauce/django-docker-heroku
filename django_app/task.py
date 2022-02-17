import time
import logging
from celery import shared_task

logger = logging.getLogger(__name__)

@shared_task(bind=True, serializer='json', retry_kwargs={'max_retries': 5, 'countdown': 60}, exponential_backoff=2)
def sample_task(self):
    """
    This is a test to simulate a task that takes a worker 3-seconds to complete
    """
    try:
        logger.info('<<<<< task starting.....')
        time.sleep(3)
        logger.info('this is an example of your task being processed w/3 second delay')
        logger.info('<<<<< task ended')
        return True
    except:
        logger.error()
        return False
