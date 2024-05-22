import sqlite3

##connect to sqlite database
conn = sqlite3.connect('EmployeeDatabase.db')

##create a cursor object using the cursor() method to retrieve records
cursor = conn.cursor()

##display the records
print("The records in the Employee table are:")

data = cursor.execute('SELECT * FROM Employee')
for row in data:
    print(row)

##close the connection
conn.close()
