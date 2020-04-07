from models import db, ImdbContent
from web_crawling import crawl_imdb_content


def load_content_to_db():
    s = db.session
    data = crawl_imdb_content()
    print(f'loading to database... total {len(data)} items')
    objects = [ImdbContent(**item) for item in data]
    s.bulk_save_objects(objects)
    s.commit()

load_content_to_db()