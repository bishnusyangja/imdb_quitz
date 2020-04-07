from urls import get_flask_app


if __name__ == '__main__':
   app = get_flask_app()
   app.run(debug=True)