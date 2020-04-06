from app import get_core_app
from home import home
from users import user_registration


def get_flask_app():
    app = get_core_app()

    app.add_url_rule('/', 'home', home, methods=['GET'])
    app.add_url_rule('/user/register/', 'user_registration', user_registration, methods=['POST'])

    return app