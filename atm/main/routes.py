from flask import Blueprint, session, render_template, url_for, flash, redirect
from flask_mail import Message
from atm import mail
from atm.main.admin import change_password
from atm.main.forms import SendEmailForm, ResetPassword
from atm.main.other import *

main = Blueprint('main', __name__)


@main.route("/home")
def home():
    if "email" in session:
        return render_template('home.html', username=username(session['email']),
                               balance=balance(session["email"]))
    else:
        return redirect(url_for('user.login'))


@main.route("/")
def about():
    return render_template('about.html', title='About')


def send_email(user):
    token = makeToken(user)
    # {url_for('reset_token', token=token, _external=True)}
    msg = Message('Password Reset', sender='no-reply@pythonatm.onthewifi.com', recipients=[user])
    msg.body = f"""To reset your password, please visit the following link
{url_for('main.reset_token', token=token, _external=True)}

This link will expire after 30 min
"""
    print(url_for('main.reset_token', token=token, _external=True))
    mail.send(msg)


@main.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if "email" in session:
        return redirect(url_for('main.home'))
    form = SendEmailForm()
    if form.validate_on_submit():
        send_email(form.email.data)
        flash('An email has been sent to reset your password', 'info')
        return redirect(url_for('user.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@main.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if "email" in session:
        return redirect(url_for('main.home'))
    user_email = verfyToken(token)
    if user_email is None:
        flash('That is an invalid or expired link', 'warning')
        return redirect(url_for('main.reset_request'))
    form = ResetPassword()
    if form.validate_on_submit():
        passw = form.password.data
        change_password(user_email, passw)
        flash(f'Password has been changed!, please log-in', 'success')
        return redirect(url_for('user.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
