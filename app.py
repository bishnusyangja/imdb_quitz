from flask import Flask
from middleware import LoginMiddleware


def get_core_app():
    app = Flask(__name__)
    app.wsgi_app = LoginMiddleware(app.wsgi_app)
    return app