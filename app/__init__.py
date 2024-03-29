from flask import Flask
from dash import Dash
import dash_bootstrap_components as dbc
import pyrebase


# Connect to Firebase:
config = {}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

# Create a Flask server:
server = Flask(__name__)
server.config.from_pyfile('config.py')

# Create a Dash app:
app = Dash(__name__,
            server=server,
            routes_pathname_prefix='/dashboard/',
            external_stylesheets=[dbc.themes.LUX])


if __name__ == '__main__':
    from views import *
    app.run_server(debug=True)
