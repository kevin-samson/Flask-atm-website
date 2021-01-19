from flask import Blueprint, session, redirect, url_for, flash, render_template, request

from atm.admin.forms import UserChangeForm, AddUser, DelUser, MakeAdmin
from atm.main.admin import is_admin, adm_Update_user, add_user, remove_user, log, \
    give_admin_perms, view_activity, iter_pages
from atm.main.other import chk_name, password, username, find_offset
from atm.users.forms import LoginForm

admin = Blueprint('admin', __name__)


@admin.route("/admin/", methods=['GET', 'POST'])
@admin.route("/admin/login", methods=['GET', 'POST'])
def login():
    if 'admin' in session:
        return redirect(url_for('admin.home'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        passw = form.password.data
        if chk_name(email) and passw == password(email) and is_admin(email):
            session["email"] = email
            session["admin"] = True
            log(f'Admin with the email {email} has logged in')
            flash('You have been logged in!', 'success')
            return redirect(url_for('admin.home'))
        if form.remember.data:
            session.permanent = True
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html', title='Login', form=form, admin=True)


@admin.route('/admin/logout')
def logout():
    if "admin" in session:
        log(f"Admin with the email {session['email']} logged out")
        session.pop("admin", None)
    if "email" in session:
        log(f"User with the email {session['email']} logged out")
        session.pop('email', None)
    return redirect(url_for('admin.login'))


@admin.route("/admin/home")
def home():
    if "email" in session and "admin" in session:
        return render_template('home.html', username=username(session['email']), admin=True)
    else:
        return redirect(url_for('admin.login'))


@admin.route('/admin/users', methods=['GET', 'POST'])
def users():
    if "email" in session and "admin" in session:
        form = UserChangeForm()
        add_form = AddUser()
        delete_form = DelUser()
        make_admin = MakeAdmin()
        if form.submit1.data and form.validate():
            adm_Update_user(form.usr_id.data, form.username.data, form.email.data)
            return redirect(url_for('admin.users'))

        if add_form.submit2.data and add_form.validate():
            add_user(add_form.username.data, add_form.email.data, 123456)
            return redirect(url_for('admin.users'))

        if delete_form.submit3.data and delete_form.validate():
            remove_user('', delete_form.usr_id.data)
            return redirect(url_for('admin.users'))

        if make_admin.submit4.data and make_admin.validate():
            if make_admin.select.data == 'yes':
                give_admin_perms(make_admin.usr_id.data, True)
            elif make_admin.select.data == 'no':
                give_admin_perms(make_admin.usr_id.data, False)
            return redirect(url_for('admin.users'))
        page = request.args.get('page', 1, type=int)
        limit, offset, pages = find_offset(page, table='user')
        return render_template('user.html', users=view_activity('user', limit=limit, offset=offset),
                               pages=iter_pages(page, pages), page=page, admin=True,
                               user_form=form, add_form=add_form, del_form=delete_form, make_admin=make_admin, logs=True)
    else:
        return redirect(url_for('admin.login'))


@admin.route("/admin/logs")
def logs():
    if "email" in session and "admin" in session:
        page = request.args.get('page', 1, type=int)
        limit, offset, pages = find_offset(page, table='transactions')
        return render_template('logs.html', logs=view_activity('transactions', limit=limit, offset=offset), admin=True,
                               transactions=True, pages=iter_pages(page, pages), page=page)
    else:
        return redirect(url_for('admin.login'))


@admin.route("/admin/bank_logs")
def bank_logs():
    if "email" in session and "admin" in session:
        page = request.args.get('page', 1, type=int)
        limit, offset, pages = find_offset(page, table='logs')
        return render_template('logs.html', logs=view_activity('logs', limit=limit, offset=offset), admin=True,
                               transactions=False, pages=iter_pages(page, pages), page=page)
    else:
        return redirect(url_for('admin.login'))
