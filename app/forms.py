from wtforms import Form
from wtforms import TextField
from wtforms.validators import DataRequired


class LoginForm(Form):
	"""Class for login form."""

	user = TextField('user', validators=[DataRequired()])
	password = TextField('password', validators=[DataRequired()])