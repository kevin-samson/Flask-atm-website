from flask import Blueprint, session, url_for, render_template, flash, request
from werkzeug.utils import redirect

from atm.bank.forms import Money
from atm.main.admin import trans_logs, remove_user
from atm.main.other import *

bank = Blueprint('bank', __name__)


@bank.route('/draw', methods=['GET', 'POST'])
def draw():
    if "email" not in session:
        return redirect(url_for('user.login'))
    else:
        form2 = Money()
        if form2.submit.data and form2.validate_on_submit():
            amont2 = form2.num.data
            session["amount"] = amont2
            session['mode'] = 'draw'
            return redirect(url_for('bank.confirmation'))

    return render_template('draw.html', title='Draw', money=form2, type='draw', tk=makeToken)


@bank.route('/deposit', methods=['GET', 'POST'])
def deposite():
    if "email" not in session:
        return redirect(url_for('user.login'))
    else:
        form2 = Money()
        if form2.submit.data and form2.validate_on_submit():
            if "amount" in session:
                session.pop("amount", None)
            amont2 = form2.num.data
            session["amount"] = amont2
            session['mode'] = 'deposit'
            return redirect(url_for('bank.confirmation'))

    return render_template('draw.html', title='Deposite', money=form2, type='deposit', tk=makeToken)


@bank.route('/confirmation')
def confirmation():
    if "email" in session:
        if "amount" in session:
            if session["mode"] == "draw":
                return render_template('confirmation.html', amount=session["amount"], mode=session["mode"], draw=True)
            elif session["mode"] == "deposit":
                return render_template('confirmation.html', amount=session["amount"], mode=session["mode"], draw=False)
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


@bank.route('/callback', methods=['GET', 'POST'])
def callback():
    # session['amount'] = int(request.args.get('amount', type=int))
    # session['mode'] = request.args.get('mode')
    session['amount'], session['mode'] = verfyToken(request.args.get('token'))
    return redirect(url_for('bank.confirmation'))
