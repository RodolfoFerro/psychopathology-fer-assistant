from flask import render_template
from flask import redirect
from flask import request
from flask import jsonify
from flask import session
from flask import url_for

from app import app
from .hash import hash_password
from .hash import verify_password_hash


@app.route('/', methods=['GET'])
def index():
    """Base URL for app."""

    # Pop previous session:
    session.pop('user', None)
    session.pop('email', None)

    return "Hello world!"
