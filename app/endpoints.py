from datetime import datetime
from collections import deque
from time import sleep

from flask import request
from flask import jsonify

from app import fer
from app import server
from app.db import MONGO_URI
from app.db import db_insert_record
from app.db import db_connect_collection


@server.route('/api/test')
def api_test():
	"""Testing URL for API."""

	return jsonify({
		'response': 'Hello world!'
	})


@server.route('/api/record', methods=['POST'])
def api_record():
	"""Recorder URL for API."""

	# Get data from JSON:
	data = request.get_json()

	record = {
			'patient': data['name'],
			'timestamp': datetime.now(),
			'anger': data['anger'],
			'disgust': data['disgust'],
			'fear': data['fear'],
			'happiness': data['happiness'],
			'sadness': data['sadness'],
			'surprise': data['surprise'],
			'neutral': data['neutral']
	}

	# Database insertion:
	db_insert_record(fer, record)

	response = {
		'response': f"Recorded a new entry at {record['timestamp']}."
	}

	return jsonify(response)


@server.errorhandler(404)
def api_test(error=None):
	return jsonify({
		'response': 'The requested url was not found.'
	})
