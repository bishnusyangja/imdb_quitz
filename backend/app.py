from celery import Celery
from flask import Flask
from flask_cors import CORS
from middleware import LoginRequiredMiddleware, AuthenticationMiddleWare


def get_core_app():
    app = Flask(__name__)
    app.wsgi_app = LoginRequiredMiddleware(app.wsgi_app)
    app.wsgi_app = AuthenticationMiddleWare(app.wsgi_app)
    CORS(app)
    return app