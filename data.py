import mysql.connector as connector

root_password="123456789" # This is the password of the user of the database (may be different for different users)

mydb = connector.connect(host='localhost', user='root', password=root_password)
mycursor = mydb.cursor()
mycursor.execute("create database if not exists atm")

db = connector.connect(host='localhost', user='root',
                       password=root_password, database='atm')
mycursor = db.cursor()
mycursor.execute(
    "create table if not exists users(card_no varchar(15), card_name varchar(30), pin varchar(6), balance int(10), primary key(card_no))")
sqlinsert = "replace into users values (%s, %s, %s, %s)"
data = [('12345678912', 'Amit Kumar', '1234', 100000), ('12345678913', 'Ayush Mishra', '4545', 10000),
        ('12345678914', 'Nidhi Rani', '7852', 50000), ('12345678915', 'Akshara Rana', '9876', 1000)]
mycursor.executemany(sqlinsert, data)
db.commit()
