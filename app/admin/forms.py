from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import User


class CompanyForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	address = StringField('Address', validators=[DataRequired()])
	submit = SubmitField('Submit')

class UserForm(FlaskForm):
	fname =  StringField('First Name', validators=[DataRequired()])
	lname = StringField('Last Name', validators=[DataRequired()])
	email = StringField('Email Address', validators=[Email(), DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Submit')

	def validate_email(self, field):
		if User.query.filter_by(email = field.data).first():
			raise ValidationError('Email is already in use.')

class UserEditForm(FlaskForm):
	first_name =  StringField('First Name', validators=[DataRequired()])
	last_name = StringField('Last Name', validators=[DataRequired()])
	submit = SubmitField('Submit')

class InviteForm(FlaskForm):
	email = StringField('Email Address', validators=[Email(), DataRequired()])
	submit = SubmitField('Submit')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email is already in use.')


class InviteEditForm(FlaskForm):
	fname =  StringField('First Name', validators=[DataRequired()])
	lname = StringField('Last Name', validators=[DataRequired()])
	email = StringField('Email Address',  render_kw={'readonly': True})
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Submit')