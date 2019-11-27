from flask import Flask


app = Flask(__name__)
app.config.from_pyfile('config.py')


if __name__ == '__main__':
    from views import *
    app.run(host='0.0.0.0', port=5000)
