

# just a home page
from flask import make_response, jsonify

from task import load_content_to_db


def home():
    load_content_to_db.delay()
    data = {"home": "Hello World"}
    return make_response(jsonify(data), 200)