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

from app import db
from app import app
from app import server
from app.forms import LoginForm
from app.hasher import hash_password
from app.hasher import verify_password_hash
from app.data_fig import generate_figure
from app.data_fig import update_data
from app.fb import fetch_last


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
		children=['Patients'],
		href='/patients',
		external_link=True
	),
	dbc.DropdownMenuItem(
		children=['About'],
		href='#',
		external_link=True,
		id='open'
	),
	dbc.Modal(
		[
			dbc.ModalHeader('About this project'),
			dbc.ModalBody(
				children=[
					dcc.Markdown(
						'''
						#### General information

						- **Patient:** John Doe
						- **Since:** 09/09/2019
						- **Last session:** 15/12/2019
						- **Diagnosis:** schizophrenia
						'''
					)
				]
			),
			dbc.ModalFooter(
				dbc.Button('Close', id='close', className='ml-auto')
			),
		],
		id='modal',
		size='lg',
		scrollable=True
	),
	dbc.DropdownMenuItem(divider=True),
	dbc.DropdownMenuItem(
		children=['Logout'],
		href='/login',
		external_link=True
	)
]

dropdowns = dbc.DropdownMenu(
	children=items,
	label='Menu',
	color='danger',
	right=True,
	className='nav-link btn btn-danger',
	nav=True,
	in_navbar=True,
	style={'text-decoration': 'none', 'padding': '0', 'color': '#FFF'}
)

nav = dbc.Nav(
	children=[
		dbc.NavItem(
			children=[
				dbc.NavLink(
					children=[
						html.Img(
							src='https://emojis.slackmojis.com/emojis/images/1450822151/257/github.png',
							style={
								'width': '15px'
							}
						),
						' GitHub Repo'
					],
					href='https://github.com/RodolfoFerro/psychopathology-fer-assistant/',
					className='nav-link btn btn-light text-dark',
					style={'margin-top': '9px'}
				)
			],
			className='nav-item mr-sm-2'
		),
		dbc.NavItem(
			children=[
				dbc.NavLink(
					children=[
						dropdowns
					],
				)
			],
			className='nav-item dropdown my-2 my-sm-0',
			style={'text-decoration': 'none', 'padding': '0'}
		)
	],
	className='navbar-nav navbar-expand-lg ml-auto flex-nowrap mt-3 mt-md-0',
	navbar=True
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
	className='navbar navbar-expand-lg navbar-dark bg-dark'
)

jumbotron = dbc.Container(
	children=[
		html.Br(),
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
		html.Br(),
		dcc.Interval(id='timer', interval=1000),
		dcc.Graph(
			id='fer-graph',
			figure=fig
		),
		html.Br(),
		html.Br(),
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

# Add callback for modal
@app.callback(
	Output('modal', 'is_open'),
	[Input('open', 'n_clicks'), Input('close', 'n_clicks')],
	[State('modal', 'is_open')],
)
def toggle_modal(n1, n2, is_open):
	if n1 or n2:
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

	return render_template('patients.html')


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
			return redirect('/patients')
		else:
			login_error = True
	return render_template('login.html', login_error=login_error)