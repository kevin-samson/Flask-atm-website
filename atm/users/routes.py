from flask import Blueprint, session, redirect, url_for, flash, render_template, request

from atm.main.admin import add_user, UpdateInfo, log, iter_pages
from atm.main.other import chk_name, password, username, view_logs, find_offset, acc_no
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

        return redirect(url_for('user.login'))
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
            log(f'User with the email {email} has logged in')
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
        log(f"User with the email {session['email']} logged out")
        session.pop("email", None)
        return redirect(url_for('user.login'))
    if "admin" in session:
        log(f"Admin with the email {session['email']} logged out")
        session.pop("admin", None)
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
    return redirect(url_for('users.login'))


@user.route('/logs')
def logs():
    if "email" in session:
        page = request.args.get('page', 1, type=int)
        limit, offset, pages = find_offset(page, table='logs', id_no=acc_no(session['email']))
        return render_template('logs.html', logs=view_logs(session['email'], limit=limit, offset=offset),
                               page=page, pages=iter_pages(page, pages))
    return redirect(url_for('users.login'))
