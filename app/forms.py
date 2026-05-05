from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')
    