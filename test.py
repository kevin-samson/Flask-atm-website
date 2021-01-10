import mysql.connector
import datetime

mydb = mysql.connector.connect(host="localhost", user="root", passwd="123456", database="atm1",
                               auth_plugin='mysql_native_password')
cur = mydb.cursor(buffered=True)

cur.execute("select * from logs where id=10")
lst=cur.fetchall()
newl = []
for i in lst[0]:
    print(i)
    newl.append(i)

print(newl)
