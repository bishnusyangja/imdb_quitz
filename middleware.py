from werkzeug.wrappers import Request, Response


class BaseMiddleware():
    '''
    Simple WSGI middleware
    '''

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        resp = self.process_request(environ, start_response)
        return resp or self.app(environ, start_response)

    def process_request(self, request, start_response):
        print("at base middleware")
        pass


class LoginMiddleware(BaseMiddleware):
    userName = ''
    password = ''

    def process_request(self, request, start_response):
        print("at login middleware")
        request_obj = Request(request)
        # userName = request_obj.authorization['username']
        # password = request_obj.authorization['password']
        return self.app(request, start_response)

        # if userName == self.userName and password == self.password:
        #     request['user'] = {'name': 'Ram'}
        #     return self.app(request, start_response)
        # else:
        #     res = Response(u'Authorization failed', mimetype='text/plain', status=401)
        #     return res(request, start_response)
