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
        self.count = 0

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

    def get_field_value(self, item, field):
        fields = field.split('.')
        if len(fields) > 1:
            value = item
            for ff in fields:
                if not (value is None or value == 'N/A'):
                    value = getattr(value, ff, 'N/A')
        else:
            value = getattr(item, field, 'N/A')
        return value

    def get_dict_from_query(self, qs):
        data = dict(results=[{field.replace('.', '_'): self.get_field_value(item,
                    field) for field in self.field_items} for item in qs])
        data['page_size'] = self.page_size
        data['page'] = self.page
        data['count'] = self.count
        return data

    def get_query_limit(self):
        page = self.request.args.get('page') or self.page
        page_size = self.request.args.get('page_size') or self.page_size
        try:
            self.page = int(page)
        except Exception as exc:
            pass
        try:
            self.page_size = int(page_size)
        except Exception as exc:
            pass

        start = (page - 1) * page_size
        end = page_size * page
        return start, end

    def get_paginated_query(self, qs):
        start, end = self.get_query_limit()
        return qs[start: end]

    def get(self):
        is_allowed, error = self.check_permission()
        if not is_allowed:
            response = make_response(jsonify(error), 403)
        else:
            qs = self.get_queryset()
            qs = self.get_paginated_query(qs)
            data = self.get_dict_from_query(qs)
            response = make_response(jsonify(data), 200)
        return response

    def post(self):
        is_allowed, error = self.check_permission()
        if not is_allowed:
            response = make_response(jsonify(error), 403)
        else:
            data = self.request.json
            errors = self.validate_fields(data)
            print(errors)
            if errors:
                response = make_response(jsonify(errors), 400)
            else:
                response = self.after_validation(data)
        return response
