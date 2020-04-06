from flask import Flask, request, make_response, jsonify
from middleware import BaseMiddleware, LoginMiddleware


def get_core_app():
    app = Flask(__name__)
    app.wsgi_app = BaseMiddleware(app.wsgi_app)
    app.wsgi_app = LoginMiddleware(app.wsgi_app)
    return app