from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])


class SettingsForm(FlaskForm):
    flow_restratio = IntegerField('Flow Rest Ratio', validators=[DataRequired()])
    pom_restratio = IntegerField('Pomodoro Rest Ratio', validators=[DataRequired()])
    pom_worklength = IntegerField('Pomodoro Work Length', validators=[DataRequired()])
    submit = SubmitField('Save')