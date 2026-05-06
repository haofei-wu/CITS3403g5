from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    IntegerField
)

from wtforms.validators import (
    DataRequired,
    Email
)


# ------------------ LOGIN FORM ------------------
class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )

    submit = SubmitField('Login')


# ------------------ REGISTER FORM ------------------
class RegisterForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )

    submit = SubmitField('Register')


# ------------------ FORGOT PASSWORD FORM ------------------
class ForgotPasswordForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )

    new_password = PasswordField(
        'New Password',
        validators=[DataRequired()]
    )

    submit = SubmitField('Reset Password')


# ------------------ SETTINGS FORM ------------------
class SettingsForm(FlaskForm):

    flow_restratio = IntegerField(
        'Flow Rest Ratio',
        validators=[DataRequired()]
    )

    pom_restratio = IntegerField(
        'Pomodoro Rest Ratio',
        validators=[DataRequired()]
    )

    pom_worklength = IntegerField(
        'Pomodoro Work Length',
        validators=[DataRequired()]
    )

    submit = SubmitField('Save')
    
