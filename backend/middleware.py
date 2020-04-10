import json

from flask import make_response, jsonify
from werkzeug.wrappers import Response

from helpers import append_slash
from settings import LOGIN_URL, USER_REGISTRATION_URL
from helpers import Anonymous


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
        print("Login Middleware")
        from models import User
        user = environ.get('IMDB_USER')
        path = environ.get('PATH_INFO')
        method = environ.get('REQUEST_METHOD')
        environ['IMDB_AUTHENTICATION'] = False
        path = append_slash(path)
        print("user", user)
        if path == LOGIN_URL or path == USER_REGISTRATION_URL or type(user) == User or method == 'OPTIONS':
            environ['IMDB_AUTHENTICATION'] = True
            return self.app(environ, start_response)
        else:
            environ['IMDB_AUTHENTICATION'] = False
            # resp = Response(json.dumps({'error': 'Authentication failed'}), mimetype='application/json', status=401)
            # resp = resp(environ, start_response)
            # resp.headers['HTTP_ACCESS_CONTROL_ALLOW_ORIGIN'] = '*'
            # resp.headers['HTTP_ACCESS_CONTROL_ALLOW_HEADERS'] = 'Authorization, Content-Type'
            # resp.headers['HTTP_ACCESS_CONTROL_ALLOW_METHODS'] = 'GET POST PUT PATCH DELETE OPTIONS'
            # print(resp.headers)
            # data = {'error': 'Authentication failed'}
            # resp = make_response(jsonify(data), 401)
            return self.app(environ, start_response)


class AuthenticationMiddleWare(BaseMiddleware):

    def get_user_from_token(self, token):
        from models import UserToken
        try:
            token = UserToken.query.filter_by(token=token)[0]
            user = token.user
        except Exception as exc:
            print("LoginExc", exc)
            user = Anonymous()
        return user

    def process_request(self, environ, start_response):
        print("Authentication Middleware")
        anonymous = Anonymous()
        print(environ)
        authorization = environ.get('HTTP_AUTHORIZATION')
        print('authorization', authorization, environ.get('PATH_INFO'), print(environ))
        token = authorization.split()[1] if authorization else ''
        environ['IMDB_USER'] = self.get_user_from_token(token) if token else anonymous
        return self.app(environ, start_response)
