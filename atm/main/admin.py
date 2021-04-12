import mysql.connector
from atm.main.other import acc_no, email

mydb = mysql.connector.connect(host="localhost", user="root", passwd="123456", database="atm1",
                               auth_plugin='mysql_native_password')
cur = mydb.cursor(buffered=True)


def log(message):
    cur.execute(f'insert into logs(description) values("{message}")')
    mydb.commit()


def iter_pages(page, pages, left_edge=2, left_current=2, right_current=5, right_edge=2):
    last = 0
    for num in range(1, pages + 1):
        if (
                num <= left_edge
                or (
                page - left_current - 1 < num < page + right_current
        )
                or num > pages - right_edge
        ):
            if last + 1 != num:
                yield None
            yield num
            last = num


def add_user(user, email, password):
    sql = "INSERT INTO USER(username,email,password,balance,admin)VALUES(%s,%s,%s,%s,%s)"
    val = (user, email, password, 1000, False)
    cur.execute(sql, val)
    mydb.commit()
    log(f'{user} with the email {email} has been added to the database')


def remove_user(email, usr_id=None):
    if email != '':
        bo = acc_no(email)
        log(f'User with email {email} has been removed from the database')
    else:
        bo = usr_id
        log(f'User with the id {usr_id} has been removed from the database')
    cur.execute(f"delete from user where id={bo}")
    mydb.commit()


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
        log(f'Username of {o_username} has been changed to {n_username}')
    if n_email == o_email:
        pass
    else:
        cur.execute(f"update user set email='{n_email}' where email='{o_email}'")
        mydb.commit()
        log(f'Email of {o_email} has been changed to {n_email}')


def change_password(email, password):
    cur.execute(f"update user set password='{password}' where email='{email}'")
    log(f'User with email {email} changed their password')
    mydb.commit()


def trans_logs(email, amount, mode):
    id_no = acc_no(email)
    sql = "INSERT INTO transactions(id,amount,type)VALUES(%s,%s,%s)"
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


def view_activity(table, limit=None, offset=None):
    if limit or offset:
        if table == 'user':
            cur.execute(f"SELECT * FROM {table} LIMIT {limit} OFFSET {offset}")
            mydb.commit()
        else:
            cur.execute(f"SELECT * FROM {table} order by date desc LIMIT {limit} OFFSET {offset} ")
            mydb.commit()
    else:
        cur.execute(f"SELECT * FROM {table}")
        mydb.commit()
    return cur.fetchall()


def adm_Update_user(usr_id, username, email):
    if username == '':
        pass
    else:
        cur.execute(f"update user set username='{username}' where id='{usr_id}'")
        mydb.commit()
        log(f'Admin has changed the username of {usr_id} to {username}')
    if email == '':
        pass
    else:
        cur.execute(f"update user set email='{email}' where id='{usr_id}'")
        log(f'Admin has changed the email of {usr_id} to {email}')


def give_admin_perms(user_id, setting):
    cur.execute(f'update user set admin={setting} where id={user_id}')
    mydb.commit()
    if setting:
        log(f"User with the email {email(user_id)} and id {user_id} is now an admin")
    else:
        log(f"User with the email {email(user_id)} and id {user_id} is removed from admin")
