from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import NumberRange, DataRequired


class Money(FlaskForm):
    num = IntegerField('', validators=[NumberRange(1, 100000)])
    submit = SubmitField('Submit')
