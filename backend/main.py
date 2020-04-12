import sys
import os
from os.path import dirname

root_path = dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(root_path))

from app import add_celery_config
from urls import get_flask_app
from task import load_content_to_db


app = get_flask_app()
celery = add_celery_config(app)
celery.conf.update(app.config)
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
