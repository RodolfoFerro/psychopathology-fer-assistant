from flask import Flask
from dash import Dash
import dash_bootstrap_components as dbc

from app.db import db_connect_collection
from app.db import MONGO_URI


# Connect to MongoDB:
fer = db_connect_collection(MONGO_URI, 'psychofer', 'fer')

# Create a Flask server:
server = Flask(__name__)
server.config.from_pyfile('config.py')

# Create a Dash app:
app = Dash(__name__,
		   server=server,
		   routes_pathname_prefix='/dashboard/',
		   external_stylesheets=[dbc.themes.BOOTSTRAP])


if __name__ == '__main__':
	from views import *
	from endpoints import *
	app.run_server(debug=True)
