from app import get_core_app
from home import home
from users import user_registration, api_auth_token


def get_flask_app():
    app = get_core_app()

    app.add_url_rule('/', 'home', home, methods=['GET'])
    app.add_url_rule('/user/register/', 'user_registration', user_registration, methods=['POST'])
    app.add_url_rule('/api/auth-token/', 'api_auth_token', api_auth_token, methods=['POST'])

    return app