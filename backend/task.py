import celery

from models import db, ImdbContent
from web_crawling import crawl_imdb_content
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@celery.task(name='imdb')
def load_content_to_db():
    s = db.session
    data = crawl_imdb_content()
    logger.info(f'loading to database... total {len(data)} items')
    objects = [ImdbContent(**item) for item in data]
    s.bulk_save_objects(objects)
    s.commit()
    return True


