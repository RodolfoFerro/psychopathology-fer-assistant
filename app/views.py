from datetime import datetime
from collections import deque
from time import sleep

import numpy as np
from flask import session
from flask import request
from flask import redirect
from flask import render_template
from dash.dependencies import State
from dash.dependencies import Input
from dash.dependencies import Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from app import fer
from app import app
from app import server
from app.forms import LoginForm
from app.hasher import hash_password
from app.hasher import verify_password_hash
from app.data_fig import generate_figure
from app.data_fig import update_data
from app.db import db_fetch_last


# Initialize dashboard data:
timestamp = deque(maxlen=20)
happiness = deque(maxlen=20)
sadness = deque(maxlen=20)
for i in range(20):
	timestamp.append(datetime.now())
	happiness.append(0)
	sadness.append(0)
	sleep(0.01)

emotions = {
	'timestamp': timestamp,
	'happiness': happiness,
	'sadness': sadness
}

# Update data from database:
update_data('John Doe', emotions)


# Create dash + Bootstrap components:
items = [
	dbc.DropdownMenuItem(
		children=[
			html.A(
				children=['Patients'],
				href='/patients',
				target='_parent',
				className='text-dark',
				style={'text-decoration': 'none'}
			)
		]
	),
	dbc.DropdownMenuItem(
		children=[
			html.A(
				children=['About'],
				href='#',
				target='_parent',
				className='text-dark',
				style={'text-decoration': 'none'}
			)
		]
	),
	dbc.DropdownMenuItem(divider=True),
	dbc.DropdownMenuItem(
		children=[
			html.A(
				children=['Logout'],
				href='/login',
				target='_parent',
				className='text-dark',
				style={'text-decoration': 'none'}
			)
		]
	)
]

dropdowns = html.Div(
	[
		dbc.DropdownMenu(
			items,
			label='Menu',
			color='primary',
			className='ml-1 flex-nowrap mt-3 mt-md-0',
			right=True
		)
	],
	style={"display": "flex", "flexWrap": "wrap"},
)


nav = dbc.Row(
	children=[
		dbc.Nav(
			children=[
				dbc.NavLink(
					children=[
						dbc.Button(
							children=[
								html.Img(
									src='https://emojis.slackmojis.com/emojis/images/1450822151/257/github.png',
									style={
										'width': '15px'
									}
								),
								' GitHub Repo'
							],
							color='light',
							className='mr-1'
						)
					],
					href='https://github.com/RodolfoFerro/psychopathology-fer-assistant/',
					className='text-dark'
				),
				dbc.NavLink(
					children=[dropdowns]
				)
			],
			navbar=True,
			justified=True
		)
	],
	no_gutters=True,
	className='ml-auto flex-nowrap mt-3 mt-md-0',
	align='center',
)

navbar = dbc.Navbar(
	children=[
		dbc.Container(
			children=[
				html.A(
					# Use row and col to control vertical alignment of logo / brand:
					dbc.Row(
						children=[
							dbc.Col(html.Img(src='../static/logo.png', height='45px')),
							dbc.Col(dbc.NavbarBrand('Psychopathology Assistant', className='ml-2')),
						],
						align='center',
						no_gutters=True,
					),
					href='/',
					target='_parent'
				),
				dbc.NavbarToggler(id='navbar-toggler'),
				dbc.Collapse(nav, id='navbar-collapse', navbar=True)
			]
		)
	],
	color='dark',
	dark=True,
	sticky='top',
)

jumbotron = dbc.Container(
	children=[
		html.Br(),
		dbc.Jumbotron(
			children=[
				html.H1('Patient Card', className='display-4'),
				dcc.Markdown(
					'''
					#### General information

					- **Patient:** John Doe
					- **Since:** 09/09/2019
					- **Last session:** 15/12/2019
					- **Diagnosis:** schizophrenia
					'''
				),
				html.P(
					'John has shown an altered perception of reality, '
					'including delusional thoughts, hallucinations, and '
					'disorganized speech and behaviour.',
					className='lead'
				),
				dbc.ButtonGroup(
					children=[
						dbc.Button(
							children=[
								html.A(
									children=['👥 Patient records'],
									href='/',
									target='_parent',
									style={'text-decoration': 'none', 'color': '#000'}
								)
							],
							color='light',
							className='md-auto text-light'
						),
						dbc.Button(
							children=[
								html.A(
									children=['📝 New record'],
									href='/',
									target='_parent',
									style={'text-decoration': 'none', 'color': '#FFF'}
								)
							],
							color='primary',
							className='md-auto text-dark'
						)
					],
				)
			]
		)
	]
)

fig = generate_figure(emotions)

plot = dbc.Container(
	children=[
		html.Br(),
		dcc.Interval(id='timer', interval=1000),
		dcc.Graph(
			id='fer-graph',
			figure=fig
		)
	]
)

body = dbc.Container(
	children=[
		dbc.Row(
			children=[
				dbc.Col(
					children=[
						jumbotron
					],
					md=5
				),
				dbc.Col(
					children=[
						plot
					],
					md=7
				)
			]
		)
	]
)


# Create dash layout by adding components:
app.layout = html.Div([navbar, body])


# Add callback for toggling the collapse on small screens
@app.callback(
	Output('navbar-collapse', 'is_open'),
	[Input('navbar-toggler', 'n_clicks')],
	[State('navbar-collapse', 'is_open')],
)
def toggle_navbar_collapse(n, is_open):
	if n:
		return not is_open
	return is_open


# Add a callback to update plot
@app.callback(output=Output('fer-graph', 'figure'),
			  inputs=[Input('timer', 'n_intervals')])
def update_graph(n_intervals):
	global emotions

	update_data('John Doe', emotions)

	fig = generate_figure(emotions)
	return fig


@server.route('/')
def index():
	"""Base URL for app."""

	# Pop previous session:
	session.pop('user', None)

	return redirect('/login')


@server.route('/patients')
def patients():
	"""Patients URL for app."""

	return '<h1>Patients section</h1>'


@server.route('/login', methods=['GET', 'POST'])
def login():
	"""Login URL for app."""

	# Pop previous session:
	session.pop('user', None)

	# Create form:
	form = LoginForm(request.form)
	login_error = False

	if len(form.errors):
		print(form.errors)
	if request.method == 'POST':
		user = form.user.data
		password = form.password.data
		if user == 'rodo_ferro' and password == 'admin':
			session['user'] = user
			return redirect('/dashboard')
		else:
			login_error = True
	return render_template('login.html', login_error=login_error)