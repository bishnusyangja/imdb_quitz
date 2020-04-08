from flask import Flask
from middleware import LoginRequiredMiddleware, AuthenticationMiddleWare


def get_core_app():
    app = Flask(__name__)
    # works in reverse order
    app.wsgi_app = LoginRequiredMiddleware(app.wsgi_app)
    app.wsgi_app = AuthenticationMiddleWare(app.wsgi_app)
    return app