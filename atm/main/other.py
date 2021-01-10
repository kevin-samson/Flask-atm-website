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


def makeToken(the_email, exp=1800):
    s = ser('5791628bb0b13ce0c676dfde280ba245', exp)
    return s.dumps({'user_id': acc_no(the_email)}).decode('utf-8')


def verfyToken(token):
    s = ser('5791628bb0b13ce0c676dfde280ba245')
    try:
        user_id = s.loads(token)['user_id']
    except:
        return None
    return email(user_id)


def view_logs(email):
    id_no = acc_no(email)
    cur.execute(f"select * from logs where id={id_no}")
    mydb.commit()
    return cur.fetchall()
