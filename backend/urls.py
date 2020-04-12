from app import get_core_app
from home import home
from quiz import score_view, quiz_view
from settings import LOGIN_URL, USER_REGISTRATION_URL
from users import user_registration, api_auth_token


def get_flask_app():
    app = get_core_app()

    app.add_url_rule('/', 'home', home, methods=['GET'])
    app.add_url_rule(USER_REGISTRATION_URL, 'user_registration', user_registration, methods=['POST'])
    app.add_url_rule(LOGIN_URL, 'api_auth_token', api_auth_token, methods=['POST'])
    app.add_url_rule('/score/list/', 'score_list', score_view, methods=['GET'])
    # app.add_url_rule('/', 'quiz_view', quiz_view, methods=['GET'])
    app.add_url_rule('/quiz/', 'quiz_view', quiz_view, methods=['GET'])
    app.add_url_rule('/quiz/<int:quiz_id>/', 'quiz_view', quiz_view, methods=['POST'])

    return app