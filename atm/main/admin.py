import mysql.connector
from atm.main.other import acc_no

mydb = mysql.connector.connect(host="localhost", user="root", passwd="123456", database="atm1",
                               auth_plugin='mysql_native_password')
cur = mydb.cursor(buffered=True)


def add_user(user, email, password):
    sql = "INSERT INTO USER(username,email,password,balance,admin)VALUES(%s,%s,%s,%s,%s)"
    val = (user, email, password, 1000, False)
    cur.execute(sql, val)
    mydb.commit()
    print(cur.rowcount, "record inserted")


def remove_user(email, usr_id=None):
    if email != '':
        bo = acc_no(email)
    else:
        bo = usr_id
    cur.execute(f"delete from user where id={bo}")
    mydb.commit()
    print("User is deleted")


def see_email(email):
    mydb.commit()
    cur.execute(f"SELECT EXISTS(SELECT * from user WHERE email='{email}')")
    mydb.commit()
    for x in cur:
        if x[0] == 0:
            return False
        else:
            return True


def see_username(username):
    mydb.commit()
    cur.execute(f"SELECT EXISTS(SELECT * from user WHERE username='{username}')")
    mydb.commit()
    for x in cur:
        if x[0] == 0:
            return False
        else:
            return True


def see_id(usr_id):
    mydb.commit()
    cur.execute(f"SELECT EXISTS(SELECT * from user WHERE username='{usr_id}')")
    mydb.commit()
    for x in cur:
        if x[0] == 0:
            return False
        else:
            return True


def UpdateInfo(n_username, n_email, o_username, o_email):
    if n_username == o_username:
        pass
    else:
        cur.execute(f"update user set username='{n_username}' where username='{o_username}'")
        mydb.commit()
    if n_email == o_email:
        pass
    else:
        cur.execute(f"update user set email='{n_email}' where email='{o_email}'")
        mydb.commit()


def change_password(email, password):
    cur.execute(f"update user set password='{password}' where email='{email}'")
    mydb.commit()


def trans_logs(email, amount, mode):
    id_no = acc_no(email)
    sql = "INSERT INTO logs(id,amount,type)VALUES(%s,%s,%s)"
    val = (id_no, amount, mode)
    cur.execute(sql, val)
    mydb.commit()


def is_admin(email):
    cur.execute(f"select admin from user where email='{email}'")
    for i in cur:
        if i[0] == 1:
            return True
        else:
            return False


def view_users():
    cur.execute(f"select * from user")
    mydb.commit()
    return cur.fetchall()


def adm_Update_user(usr_id, username, email):
    if username == '':
        pass
    else:
        cur.execute(f"update user set username='{username}' where id='{usr_id}'")
        mydb.commit()
    if email == '':
        pass
    else:
        cur.execute(f"update user set email='{email}' where id='{usr_id}'")
        mydb.commit()
