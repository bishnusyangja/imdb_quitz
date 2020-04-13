import sys
import os
from os.path import dirname

from celery import Celery

from settings import DB_PATH, DB_NAME

root_path = dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(root_path))

from urls import get_flask_app


app = get_flask_app()
app.config.update(
    CELERY_BROKER_URL='redis://127.0.0.1:6379/5',
    CELERY_RESULT_BACKEND='redis://127.0.0.1:6379/5',
    # CELERY_BACKEND_URL='redis://127.0.0.1:6379/5',
    # CELERY_BACKEND_URL='http://localhost:5000'
)


def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery


celery = make_celery(app)

# app.config.broker_transport_options = {
#     'max_retries': 3,
#     'interval_start': 0,
#     'interval_step': 0.2,
#     'interval_max': 0.2,
#     'visibility_timeout': 3600,
# }


# app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
# app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
# celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# celery.conf.update(app.config)

# the task starts after countdown seconds



# if __name__ == '__main__':
#    app.run(debug=True)


# todo: remove quiz_attempted = 0
# todo: migrate is_submitted in quiz models
# todo: check is_submitted in quiz post check permission
# todo: update is_submitted after getting score
# todo: radio button not working in quiz list
# todo: bulk update question's answer
# todo: pagination_custom in antd table
