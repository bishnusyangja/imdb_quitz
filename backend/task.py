from celery_app import celery


from web_crawling import crawl_imdb_content
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@celery.task
def load_content_to_db():
    from models import db, ImdbContent
    logger.info("content loading")
    s = db.session
    data = crawl_imdb_content()
    logger.info(f'loading to database... total {len(data)} items')
    objects = [ImdbContent(**item) for item in data]
    s.bulk_save_objects(objects)
    s.commit()
    return True


@celery.task
def abc():
    print("abc task")
    logger.info("abc task")
    a = 2
    b = 3
    print('a+b =', a+b)
    logger.info('a+b =', a+b)
    return True


from celery.worker import consumer