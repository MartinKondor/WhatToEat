import os
from flask import Flask, render_template
from src.cook import Cook


APP = Flask(__name__)
HOST = '127.0.0.1'
PORT = int(os.environ.get('PORT', 5000))
DEBUG = False if os.environ.get('IS_HEROKU', False) else True
COOK = Cook()


@APP.route('/')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    APP.run(debug=DEBUG, host=HOST, port=PORT)
