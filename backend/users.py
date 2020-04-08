from flask import request, make_response, jsonify

from helpers import truncate_line, get_random_string
from models import db, User, UserToken
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

        if not data.get('password') == data.get('confirm_password'):
            errors['password'] = 'Password does not match'
        return errors

    def validate_user_code(self, user_code):
        file_path = 'code_files.txt'
        with open(file_path, 'r') as fp:
            content = fp.readlines()
            content = [truncate_line(line) for line in content]
            return user_code.strip() in content

    def after_validation(self, data):
        self.create_user(data['username'], data['name'], data['password'])
        status = 201
        response = {}
        return make_response(jsonify(response), status)

    def create_user(self, username, name, password):
        data = dict(username=username, name=name)
        user = User(**data)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()


class ApiAuthView(BaseView):

    def get_user_obj(self, username):
        try:
            obj = User.query.filter_by(username=username)
            if len(obj) > 1:
                user = None
            user = user[0]
        except Exception as e:
            user = None
        return user

    def validate_fields(self, data):
        errors = {}
        username = data.get('username')
        user = self.get_user_obj(username)
        if user is None:
            errors['user'] = 'Username or password doesnot match'
        else:
            password = data.get('password')
            if not user.check_password(password):
                errors['user'] = 'Username or password doesnot match'
        return errors

    def get_auth_token(self):
        try:
            obj = UserToken.query.filter_by(user_id=self.user.id)[0]
        except UserToken.DoesNotExist:
            obj = UserToken(user_id=self.user.id, token=get_random_string())
        db.session.add(obj)
        db.session.commit()
        return obj.token

    def after_validation(self, data):
        status = 200
        response = {'token': self.get_auth_token()}
        return make_response(jsonify(response), status)


def user_registration():
    view = UserRegistrationView(request)
    return view.get_response()


def api_auth_token():
    view = ApiAuthView(request)
    return view.get_response()