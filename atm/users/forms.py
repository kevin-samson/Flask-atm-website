from flask import session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from atm.main.other import username
from atm.main.admin import see_email, see_username


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=60)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password'), Length(min=6, max=60)])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        see = email.data
        if see_email(see):
            raise ValidationError("Email is alredy taken")

    def validate_username(self, username):
        see = username.data
        if see_username(see):
            raise ValidationError("Username is alredy taken")


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UserChangeForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(min=2, max=100)])
    submit = SubmitField('Update Account')

    def validate_email(self, email):
        if email.data != session['email']:
            see = email.data
            if see_email(see):
                raise ValidationError("Email is already taken")

    def validate_username(self, user):
        if user.data != username(session['email']):
            see = user.data
            if see_username(see):
                raise ValidationError("Username is already taken")

    delete = SubmitField('Delete Account')
    reset_pass = SubmitField('Reset Password')
