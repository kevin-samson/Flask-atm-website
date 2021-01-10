from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField


class CusForm(FlaskForm):
    submit = SubmitField('Submit')
    b50 = SubmitField('50')
    b100 = SubmitField('100')
    b250 = SubmitField('250')
    b500 = SubmitField('500')
    b1000 = SubmitField('1000')


class Money(FlaskForm):
    num = IntegerField('')
    submit = SubmitField('Submit')