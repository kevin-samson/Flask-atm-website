from math import ceil

import mysql.connector
from itsdangerous import TimedJSONWebSignatureSerializer as ser

mydb = mysql.connector.connect(host="localhost", user="root", passwd="123456", database="atm1",
                               auth_plugin='mysql_native_password')
cur = mydb.cursor(buffered=True)


def acc_no(email):
    cur.execute("select email from user")
    mydb.commit()
    for x in cur:
        if x[0].lower() == email.lower():
            cur.execute(f"select id from user where email='{email}'")
            for i in cur:
                return i[0]


def chk_name(name):
    mydb.commit()
    cur.execute(f"select id from user where email= '{name}'")
    mydb.commit()
    data = 0
    for x in cur:
        data = x
    if data == 0:
        return False
    else:
        return True


def password(name):
    account_no = acc_no(name)
    cur.execute(f"select password from user where id={account_no}")
    mydb.commit()
    for i in cur:
        return i[0]


def balance(name):
    account_no = acc_no(name)
    cur.execute(f"select balance from user where id={account_no}")
    mydb.commit()
    for i in cur:
        return i[0]


def email(num):
    cur.execute(f"select email from user where id={num}")
    mydb.commit()
    for i in cur:
        return i[0]


def username(email):
    account_no = acc_no(email)
    cur.execute(f"select username from user where id={account_no}")
    mydb.commit()
    for i in cur:
        return i[0]


def drawAmount(name, amount):
    while True:
        try:
            amount = int(amount)
            if amount > balance(name):
                raise
        except:
            print("Invalid amount")

            break
        new_amount = balance(name) - amount
        cur.execute(f"update user set balance={new_amount} where id={acc_no(name)}")
        mydb.commit()
        print("Amount has been drawn")
        break


def depositeAmount(name, amount):
    global new_amount
    while True:
        try:
            amount = int(amount)
        except:
            print("\nInvalid amount")
            break
        if balance(name) is None:
            new_amount = amount
        elif balance(name) is not None:
            new_amount = balance(name) + amount
        cur.execute(f"update user set balance={new_amount} where id={acc_no(name)}")
        mydb.commit()
        print("Amount has been deposited")
        break


def makeToken(the_email, exp=1800, amount=None, mode=None):
    if the_email != '':
        s = ser('5791628bb0b13ce0c676dfde280ba245', exp)
        return s.dumps({'email': the_email}).decode('utf-8')
    elif amount and mode:
        s = ser('5791628bb0b13ce0c676dfde280ba245', exp)
        return s.dumps({'mode': mode, 'amount': amount}).decode('utf-8')


def verfyToken(token):
    s = ser('5791628bb0b13ce0c676dfde280ba245')
    try:
        data = s.loads(token)
    except:
        return None
    if data:
        if 'email' in data:
            the_email = s.loads(token)['user_id']
            return the_email
        elif 'mode' in data:
            return s.loads(token)['amount'], s.loads(token)['mode']


def view_logs(email, limit, offset):
    id_no = acc_no(email)
    cur.execute(f"select * from transactions where id={id_no} order by date desc LIMIT {limit} OFFSET {offset}")
    mydb.commit()
    return cur.fetchall()


def total_rows(table, id_no=None):
    if id_no:
        cur.execute(f'select count(*) from transactions where id={id_no}')
        mydb.commit()
    else:
        cur.execute(f'select count(*) from {table}')
        mydb.commit()
    return cur.fetchall()[0][0]


def find_offset(page, table, per_page=7, id_no=None):
    pages = int(ceil(total_rows(table, id_no) / float(per_page)))
    offset = (page - 1) * per_page
    limit = 7 if page == pages else per_page
    return limit, offset, pages
