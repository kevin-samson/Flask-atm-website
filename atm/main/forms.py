from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length

from atm.main.admin import see_email


class SendEmailForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        see = email.data
        if see_email(see) is False:
            raise ValidationError("There is no account with that email.You need to register first")


class ResetPassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=60)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password'), Length(min=6, max=60)])
    submit = SubmitField('Reset Password')