from flask import make_response, jsonify

from settings import DEFAULT_PAGE_SIZE


class BaseView:

    field_items = ()
    page_size = DEFAULT_PAGE_SIZE
    page = 1

    def __init__(self, request):
        self.user = request.environ.get('IMDB_USER')
        self.request = request

    def check_permission(self):
        return True, {}

    def get_queryset(self):
        return []

    def get_response(self):
        if self.request.method == 'GET':
            return self.get()
        elif self.request.method == 'POST':
            return self.post()
        else:
            return make_response(jsonify(dict(error='Method not allowed')), 405)

    def validate_fields(self, data):
        return make_response(jsonify(dict(error='Not Implemented')), 500)

    def after_validation(self, data):
        return make_response(jsonify(dict(error='Not Implemented')), 500)

    def get(self):
        is_allowed, error = self.check_permission()
        if not is_allowed:
            return make_response(jsonify(error), 403)
        qs = self.get_queryset()
        data = [{key: item[key] for key in self.field_items} for item in qs]
        return make_response(jsonify(data), 200)

    def post(self):
        is_allowed, error = self.check_permission()
        if not is_allowed:
            return make_response(jsonify(error), 403)
        data = self.request.json
        errors = self.validate_fields(data)
        if errors:
            return make_response(jsonify(errors), 400)
        else:
            return self.after_validation(data)
