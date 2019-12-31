import numpy as np

from app import db
from app.fb import fetch_last


def update_data(patient, emotions):
	latest_data = fetch_last(db, 'fer')
	latest_data = [entry.val() for entry in latest_data.each()][::-1]
	
	for item in latest_data:
		emotions['timestamp'].append(item['timestamp'])
		emotions['anger'].append(item['anger'])
		emotions['disgust'].append(item['disgust'])
		emotions['fear'].append(item['fear'])
		emotions['happiness'].append(item['happiness'])
		emotions['sadness'].append(item['sadness'])
		emotions['surprise'].append(item['surprise'])
		emotions['neutral'].append(item['neutral'])
	
	return


def generate_figure(emotions):

	return {
		'data': [
			dict(
				x=np.array(emotions['timestamp']),
				y=np.array(emotions[key]),
				name=f"{key}",
				# marker=dict(
				# 	color='rgb(55, 83, 109)'
				# ),
				line=dict(
					shape='spline'
				)
			) for key in emotions.keys() if key != 'timestamp'
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