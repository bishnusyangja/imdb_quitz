from celery import Celery
from flask import Flask
from flask_cors import CORS
from middleware import LoginRequiredMiddleware, AuthenticationMiddleWare


def add_celery_config(app):
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
    celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
    return celery


def get_core_app():
    app = Flask(__name__)
    app.wsgi_app = LoginRequiredMiddleware(app.wsgi_app)
    app.wsgi_app = AuthenticationMiddleWare(app.wsgi_app)
    CORS(app)
    return app