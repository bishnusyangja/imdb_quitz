from flask import request, make_response, jsonify


def validate_user_code(user_code):
    file_path='code_files.txt'
    # todo: validate user codes
    with open(file_path, 'r') as fp:
        fp.read()
    return True


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
    pass


def user_registration():
    data = request.json
    username = data.get('username')
    user_code = data.get('code')
    name = data.get('name')
    if validate_fields(username, user_code, name):
        return make_response(jsonify({'error': 'username, user_code and name is required'}), 400)
    if not validate_user_code(user_code):
        return make_response(jsonify({'error': 'username, user_code and name is required'}), 400)
    create_user(username, name)
    status = 201
    response = {}
    return make_response(jsonify(response), status)