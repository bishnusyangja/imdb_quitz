from flask import request, make_response, jsonify

from helpers import truncate_line
from models import db, User
from views import BaseView


class UserRegistrationView(BaseView):

    def validate_fields(self, data):
        errors = {}
        if not data.get('username'):
            errors['username'] = 'username is required'
        if not data.get('name'):
            errors['name'] = 'name is required'
        if not data.get('user'):
            errors['code'] = 'code is required'
        elif not self.validate_user_code(data.get('code')):
            errors['code'] = 'The code you submitted is not valid'
        return errors

    def validate_user_code(self, user_code):
        file_path = 'code_files.txt'
        with open(file_path, 'r') as fp:
            content = fp.readlines()
            content = [truncate_line(line) for line in content]
            return user_code.strip() in content

    def after_validation(self, data):
        self.create_user(data['username'], data['name'])
        status = 201
        response = {}
        return make_response(jsonify(response), status)

    def create_user(self, username, name):
        data = dict(username=username, name=name)
        db.session.add(User(**data))
        db.session.commit()


def user_registration():

    view = BaseView(request)
    return view.get_response()
