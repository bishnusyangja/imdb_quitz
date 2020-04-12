from flask import make_response, jsonify

from settings import DEFAULT_PAGE_SIZE


class BaseView:

    field_items = ()
    page_size = DEFAULT_PAGE_SIZE
    page = 1

    def __init__(self, request):
        self.user = request.environ.get('IMDB_USER')
        self.request = request
        self.is_authenticated = request.environ.get('IMDB_AUTHENTICATION', False)

    def check_permission(self):
        return True, {}

    def get_queryset(self):
        return []

    def initite_view(self):
        if not self.is_authenticated:
            errors = {'error': 'Authentication failed'}
            return make_response(jsonify(errors), 401)
        if self.request.method == 'GET':
            return self.get()
        elif self.request.method == 'POST':
            return self.post()
        else:
            return make_response(jsonify(dict(error='Method not allowed')), 405)

    def get_response(self):
        try:
            resp = self.initite_view()
        except Exception as exc:
            print('Excep 500 ', exc)
            resp = make_response(jsonify(dict(error='Server Error')), 500)
        return resp

    def validate_fields(self, data):
        return {make_response(jsonify(dict(error='Not Implemented')), 500)}

    def after_validation(self, data):
        return make_response(jsonify(dict(error='Not Implemented')), 500)

    def get(self):
        is_allowed, error = self.check_permission()
        if not is_allowed:
            response = make_response(jsonify(error), 403)
        else:
            qs = self.get_queryset()
            data = [{key: getattr(item, key, 'N/A') for key in self.field_items} for item in qs]
            response = make_response(jsonify(data), 200)
        return response

    def post(self):
        is_allowed, error = self.check_permission()
        if not is_allowed:
            response = make_response(jsonify(error), 403)
        else:
            data = self.request.json
            errors = self.validate_fields(data)
            if errors:
                response = make_response(jsonify(errors), 400)
            else:
                response = self.after_validation(data)
        return response
