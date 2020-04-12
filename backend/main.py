import sys
import os
from os.path import dirname
root_path = dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(root_path))


from urls import get_flask_app

app = get_flask_app()

# @app.after_request
# def after_request(response):
#   response.headers.add('Access-Control-Allow-Origin', '*')
#   response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#   response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
#   return response

# if __name__ == '__main__':
#    app.run(debug=True)


# todo: remove quiz_attempted = 0
# todo: migrate is_submitted in quiz models
# todo: check is_submitted in quiz post check permission
# todo: update is_submitted after getting score
# todo: radio button not working in quiz list
# todo: bulk update question's answer
# todo: pagination_custom in antd table
