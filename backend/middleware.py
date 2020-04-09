import json
from werkzeug.wrappers import Response

from helpers import append_slash
from settings import LOGIN_URL, USER_REGISTRATION_URL
from models import User, UserToken, Anonymous


class BaseMiddleware:
    """
    Base Middleware for our IMDB quiz system
    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        resp = self.process_request(environ, start_response)
        return resp or self.app(environ, start_response)

    def process_request(self, request, start_response):
        pass


class LoginRequiredMiddleware(BaseMiddleware):

    def process_request(self, environ, start_response):
        user = environ.get('IMDB_USER')
        path = environ.get('PATH_INFO')
        path = append_slash(path)
        if path == LOGIN_URL or path == USER_REGISTRATION_URL or type(user) == User:
            return self.app(environ, start_response)
        else:
            Response(json.dumps({'Authorization failed'}), mimetype='application/json', status=401)


class AuthenticationMiddleWare(BaseMiddleware):

    def get_user_from_token(self, token):
        try:
            token = UserToken.query.filter_by(token=token)[0]
            user = token.user
        except Exception as exc:
            print("LoginExc", exc)
            user = Anonymous()
        return user

    def process_request(self, environ, start_response):
        anonymous = Anonymous()
        authorization = environ.get('HTTP_AUTHORIZATION')
        token = authorization.split()[1] if authorization else ''
        environ['IMDB_USER'] = self.get_user_from_token(token) if token else anonymous
        return self.app(environ, start_response)
