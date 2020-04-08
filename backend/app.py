from flask import Flask
from flask_cors import CORS

from middleware import LoginRequiredMiddleware, AuthenticationMiddleWare

def get_core_app():
    app = Flask(__name__)
    CORS(app, resources={r"*": {"origins": "http://localhost:3000"}})
    # works in reverse order
    app.wsgi_app = LoginRequiredMiddleware(app.wsgi_app)
    app.wsgi_app = AuthenticationMiddleWare(app.wsgi_app)
    # CORS(app, support_credentials=True)
    # app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
    # app.config['CORS_HEADERS'] = 'Content-Type'

    return app