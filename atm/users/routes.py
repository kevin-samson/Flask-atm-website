from flask import Blueprint, session, redirect, url_for, flash, render_template

from atm.main.admin import add_user, UpdateInfo
from atm.main.other import chk_name, password, username, view_logs
from atm.users.forms import RegistrationForm, LoginForm, UserChangeForm

user = Blueprint('user', __name__)


@user.route("/register", methods=['GET', 'POST'])
def register():
    if 'email' in session:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = form.username.data
        email = form.email.data
        passw = form.password.data
        add_user(user, email, passw)
        flash(f'Account created for {form.username.data}! please log-in', 'success')

        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)


@user.route("/login", methods=['GET', 'POST'])
def login():
    if 'email' in session:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        passw = form.password.data
        if chk_name(email) == True and passw == password(email):
            session["email"] = email
            flash('You have been logged in!', 'success')
            return redirect(url_for('main.home'))
        if form.remember.data:
            session.permanent = True
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html', title='Login', form=form)


@user.route('/logout')
def logout():
    if "email" in session:
        session.pop("email", None)
        return redirect(url_for('user.login'))


@user.route('/account', methods=['GET', 'POST'])
def account():
    if 'email' in session:
        form = UserChangeForm()

        if form.validate_on_submit():
            if form.delete.data:
                session['amount'] = ''
                session['mode'] = ''
                return redirect(url_for('bank.confirmation'))
            if form.reset_pass.data:
                session.pop('email', None)
                return redirect(url_for('main.reset_request'))

            user = form.username.data
            email1 = form.email.data
            UpdateInfo(user, email1, username(session['email']), session['email'])
            flash('Changes have been made, please log-in again', 'success')
            session.pop("email", None)
            return redirect(url_for('main.home'))
        else:
            form.username.data = username(session['email'])
            form.email.data = session['email']
        return render_template('account.html', username=username(session['email']), email=session['email'], form=form)
    return redirect(url_for('main.login'))


@user.route('/logs')
def logs():
    if "email" in session:
        return render_template('logs.html', logs=view_logs(session['email']))
    return redirect(url_for('main.login'))
