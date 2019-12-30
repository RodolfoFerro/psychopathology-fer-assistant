from flask import render_template
from flask import redirect
from flask import request
from flask import jsonify
from flask import session
from flask import url_for
from dash.dependencies import State
from dash.dependencies import Input
from dash.dependencies import Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from app import app
from app import server
from app.hasher import hash_password
from app.hasher import verify_password_hash


# Create dash + Bootstrap components:
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
										'width': '25px'
									}
								),
								' GitHub Repo'
							],
							color='light',
							className='mr-1')
					],
					href='https://github.com/RodolfoFerro/psychopathology-fer-assistant/',
					className='text-dark'
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
				html.H1('Demo App', className='display-3'),
				html.P(
					'This is a demo application to '
					'test Dash with Bootstrap integration.',
					className='lead',
				),
				html.A(
					children=[
						dbc.Button(
							children=[
								html.Img(
									src='https://emojis.slackmojis.com/emojis/images/1450822151/257/github.png',
									style={
										'width': '25px'
									}
								),
								' GitHub Repo'
							],
							color='light',
							className='mr-1')
					],
					href='https://github.com/RodolfoFerro/psychopathology-fer-assistant/',
					className='text-dark'
				)
			]
		)
	]
)

plot = dbc.Container(
	children=[
		html.Br(),
		dcc.Graph(
			figure={
				'data': [
					dict(
						x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
							2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
						y=[219, 146, 112, 127, 124, 180, 236, 207, 236, 263,
							350, 430, 474, 526, 488, 537, 500, 439],
						name='Rest of world',
						marker=dict(
							color='rgb(55, 83, 109)'
						)
					),
					dict(
						x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
							2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
						y=[16, 13, 10, 11, 28, 37, 43, 55, 56, 88, 105, 156, 270,
							299, 340, 403, 549, 499],
						name='China',
						marker=dict(
							color='rgb(26, 118, 255)'
						)
					)
				],
				'layout': dict(
					title='US Export of Plastic Scrap',
					showlegend=True,
					legend=dict(
						x=0,
						y=1.0
					),
					margin=dict(l=40, r=0, t=40, b=30)
				)
			}
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


# add callback for toggling the collapse on small screens
@app.callback(
	Output('navbar-collapse', 'is_open'),
	[Input('navbar-toggler', 'n_clicks')],
	[State('navbar-collapse', 'is_open')],
)
def toggle_navbar_collapse(n, is_open):
	if n:
		return not is_open
	return is_open


@server.route('/')
def index():
	"""Base URL for app."""

	# Pop previous session:
	session.pop('user', None)
	session.pop('email', None)

	return redirect('/')
