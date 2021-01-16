from flask import session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, RadioField
from wtforms.validators import DataRequired, Length, Email, ValidationError, Optional, EqualTo

from atm.main.admin import see_email, see_username, see_id
from atm.main.other import username


class UserChangeForm(FlaskForm):
    usr_id = IntegerField('ID', validators=[DataRequired()])
    username = StringField('Username',
                           validators=[Optional(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[Optional(), Email()])
    submit1 = SubmitField('Update Account')

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

    def validate_id(self, usr_id):
        see = usr_id.data
        if see_id(see):
            raise ValidationError("ID is already taken")


class AddUser(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    # password = PasswordField('Password', validators=[DataRequired()])
    # confirm_password = PasswordField('Confirm Password',
    # validators=[DataRequired(), EqualTo('password')])
    submit2 = SubmitField('Submit')

    def validate_email(self, email):
        see = email.data
        if see_email(see):
            raise ValidationError("Email is alredy taken")

    def validate_username(self, username):
        see = username.data
        if see_username(see):
            raise ValidationError("Username is alredy taken")


class DelUser(FlaskForm):
    usr_id = IntegerField('ID', validators=[DataRequired()])
    submit3 = SubmitField('Submit')

    def validate_usr_id(self, usr_id):
        see = usr_id.data
        if see_id(see):
            raise ValidationError("ID does not exist")


class MakeAdmin(FlaskForm):
    usr_id = IntegerField('ID', validators=[DataRequired()])
    select = RadioField(choices=[('yes', 'Make Admin'), ('no', 'Remove Admin')], validators=[DataRequired()])
    submit4 = SubmitField('Submit')

    def validate_usr_id(self, usr_id):
        see = usr_id.data
        if see_id(see):
            raise ValidationError("ID does not exist")
