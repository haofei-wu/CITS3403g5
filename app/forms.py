from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password', message='Passwords must match')]
    )
    submit = SubmitField('Register')

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('new_password', message='Passwords must match')]
    )
    submit = SubmitField('Reset Password')

class SettingsForm(FlaskForm):
    nickname = StringField('Nickname', validators=[DataRequired(), Length(min=1, max=64)])
    flow_restratio = IntegerField('Flow Rest Ratio', validators=[DataRequired()])
    pom_worklength = IntegerField('Pomodoro Work Length', validators=[DataRequired()])
    pom_short_break = IntegerField('Pomodoro Short Break Length', validators=[DataRequired()])
    pom_long_break = IntegerField('Pomodoro Long Break Length', validators=[DataRequired()])
    submit = SubmitField('Save')

class profileform(FlaskForm):
    avatar= FileField(
        'Avatar', 
        validators=[FileAllowed(['jpg', 'png','jpeg'], 'Images only')]
        )
    submit = SubmitField('Save')
