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