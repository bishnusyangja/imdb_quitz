

# just a home page
from flask import make_response, jsonify

# from task import load_content_to_db


def home():
    from task import load_content_to_db
    from task import abc
    abc.delay()
    data = {"home": "Hello World"}
    return make_response(jsonify(data), 200)