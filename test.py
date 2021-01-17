import mysql.connector

from atm.main.other import acc_no

mydb = mysql.connector.connect(host="localhost", user="root", passwd="123456", database="atm1",
                               auth_plugin='mysql_native_password')
cur = mydb.cursor(buffered=True)

def view_logs():

    cur.execute(f"select * from transactions where id=35 order by date desc;select count(*) from logs")
    mydb.commit()
    return cur.fetchall()

print(view_logs())