from flask import Blueprint, session, url_for, render_template, flash
from werkzeug.utils import redirect

from atm.bank.forms import CusForm, Money
from atm.main.admin import trans_logs, remove_user
from atm.main.other import *

bank = Blueprint('bank', __name__)


@bank.route('/draw', methods=['GET', 'POST'])
def draw():
    if "email" not in session:
        return redirect(url_for('user.login'))
    else:
        form = CusForm()
        form2 = Money()
        if form.validate_on_submit():
            session["mode"] = "draw"
            if form.b50.data:
                session["amount"] = 50
                return redirect(url_for('bank.confirmation'))
            elif form.b100.data:
                session["amount"] = 100
                return redirect(url_for('bank.confirmation'))
            elif form.b250.data:
                session["amount"] = 250
                return redirect(url_for('bank.confirmation'))
            elif form.b500.data:
                session["amount"] = 500
                return redirect(url_for('bank.confirmation'))
            elif form.b1000.data:
                session["amount"] = 1000
                return redirect(url_for('bank.confirmation'))
        if form2.submit.data and form2.validate_on_submit():
            amont2 = form2.num.data
            session["amount"] = amont2
            return redirect(url_for('bank.confirmation'))

    return render_template('draw.html', title='Draw', form=form, money=form2)


@bank.route('/deposit', methods=['GET', 'POST'])
def deposite():
    if "email" not in session:
        return redirect(url_for('user.login'))
    else:
        form = CusForm()
        form2 = Money()
        if form.validate_on_submit():
            session["mode"] = "deposit"
            if form.b50.data:
                session["amount"] = 50
                return redirect(url_for('bank.confirmation'))
            elif form.b100.data:
                session["amount"] = 100
                return redirect(url_for('bank.confirmation'))
            elif form.b250.data:
                session["amount"] = 250
                return redirect(url_for('bank.confirmation'))
            elif form.b500.data:
                session["amount"] = 500
                return redirect(url_for('bank.confirmation'))
            elif form.b1000.data:
                session["amount"] = 1000
                return redirect(url_for('bank.confirmation'))

        if form2.submit.data and form2.validate_on_submit():
            if "amount" in session:
                session.pop("amount", None)
            amont2 = form2.num.data
            print(session)
            session["amount"] = amont2
            return redirect(url_for('bank.confirmation'))

    return render_template('draw.html', title='Deposite', form=form, money=form2)


@bank.route('/confirmation')
def confirmation():
    if "email" in session:
        if "amount" in session:
            if session["mode"] == "draw":
                return render_template('confirmation.html', amount=session["amount"], mode=session["mode"])
            elif session["mode"] == "deposit":
                return render_template('confirmation.html', amount=session["amount"], mode=session["mode"])
            elif session["amount"] == '':
                return render_template('confirmation.html', amount=session["amount"])

        return redirect(url_for('main.home'))
    return redirect(url_for('user.login'))


@bank.route('/landing')
def success():
    if "email" in session:
        if "amount" in session:
            if session['amount'] == '':
                remove_user(session['email'])
                session.pop('email')
                flash('Account is deleted :(', 'info')
                return redirect(url_for('main.home'))
            else:
                if session["mode"] == "draw":
                    if balance(session["email"]) is None or session['amount'] > balance(session["email"]):
                        flash("Insufficient funds", "danger")
                        return redirect(url_for("main.home"))
                    drawAmount(session["email"], session["amount"])
                    trans_logs(session["email"], session["amount"], "DRAW")
                    session.pop("amount", None)
                    session.pop("mode", None)
                    return render_template('trans-comp.html', message="Amount has been drawn")

                elif session["mode"] == "deposit":
                    depositeAmount(session["email"], session["amount"])
                    trans_logs(session["email"], session["amount"], "DEPOSIT")
                    session.pop("amount")
                    return render_template('trans-comp.html', message="Amount has been deposited")
        else:
            return redirect(url_for('main.home'))
    else:
        return redirect(url_for('user.login'))
