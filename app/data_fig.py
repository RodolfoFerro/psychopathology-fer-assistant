import numpy as np

from app import db
from app.fb import fetch_last


def update_data(patient, emotions):
	latest_data = fetch_last(db, 'fer')
	latest_data = [entry.val() for entry in latest_data.each()][::-1]

	if 0 < len(latest_data) < 20:
		emotions['timestamp'].append(latest_data[-1]['timestamp'])
		emotions['happiness'].append(latest_data[-1]['happiness'])
		emotions['sadness'].append(latest_data[-1]['sadness'])
	else:
		for item in latest_data:
			emotions['timestamp'].append(item['timestamp'])
			emotions['happiness'].append(item['happiness'])
			emotions['sadness'].append(item['sadness'])
	
	return


def generate_figure(emotions):
	return {
		'data': [
			dict(
				x=np.array(emotions['timestamp']),
				y=np.array(emotions['happiness']),
				name='Happiness',
				marker=dict(
					color='rgb(55, 83, 109)'
				),
				line=dict(
					shape='spline'
				)
			),
			dict(
				x=np.array(emotions['timestamp']),
				y=np.array(emotions['sadness']),
				name='Saddness',
				marker=dict(
					color='rgb(26, 118, 255)'
				),
				line=dict(
					shape='spline'
				)
			)
		],
		'layout': dict(
			title='General FER Activity',
			showlegend=True,
			legend=dict(
				x=0,
				y=1.0
			),
			margin=dict(l=40, r=0, t=40, b=30)
		)
	}