from flask import request, make_response, jsonify
from models import db, User


def truncate_line(line):
    return line.replace('\n').strip()


def validate_user_code(user_code):
    file_path='code_files.txt'
    with open(file_path, 'r') as fp:
        content = fp.readlines()
        content = [truncate_line(line) for line in content]
        return user_code.strip() in content


def validate_fields(username, user_code, name):
    errors = {}
    if not username:
        errors['username'] = 'username is required'
    if not user_code:
        errors['user_code'] = 'user_code is required'
    if not name:
        errors['name'] = 'name is required'
    return errors


def create_user(username, name):
    data = dict(username=username, name=name)
    db.session.add(User(**data))
    db.session.commit()


def user_registration():
    data = request.json
    username = data.get('username')
    user_code = data.get('code')
    name = data.get('name')
    errors = validate_fields(username, user_code, name)
    if errors:
        return make_response(jsonify(errors), 400)
    if not validate_user_code(user_code):
        return make_response(jsonify({'code': 'the code you have provided is not valid'}), 400)
    create_user(username, name)
    status = 201
    response = {}
    return make_response(jsonify(response), status)


validate_user_code('')