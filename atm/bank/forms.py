from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import NumberRange, DataRequired


class CusForm(FlaskForm):
    b50 = SubmitField('50')
    b100 = SubmitField('100')
    b250 = SubmitField('250')
    b500 = SubmitField('500')
    b1000 = SubmitField('1000')


class Money(FlaskForm):
    num = IntegerField('', validators=[NumberRange(1, 100000)])
    submit = SubmitField('Submit')
