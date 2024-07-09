import sqlite3

## Connect to sqlite
connection=sqlite3.connect("student.db")

## Create a curosr object to insert record,create table,retrive
cursor=connection.cursor()

## Create the table
table_info='''
Create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),SECTION
VARCHAR(25),MARKS INT);'''


cursor.execute(table_info)

## Insert some more records

cursor.execute('''Insert into STUDENT values('Krish','Data Science','A',90)''')
cursor.execute('''Insert into STUDENT values('Naik','Data Science','B',100)''')
cursor.execute('''Insert into STUDENT values('Darius','Data Science','A',86)''')
cursor.execute('''Insert into STUDENT values('Vikash','Data Science','A',50)''')
cursor.execute('''Insert into STUDENT values('Abishek','Data Science','A',60)''')

## Display all the records
print("The inserted records are")

data = cursor.execute('''Select * From STUDENT''')

for row in data:
    print(row)

## Close the connection

connection.commit()
connection.close()
