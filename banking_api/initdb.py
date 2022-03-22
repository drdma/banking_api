"""Initialise database with given data."""
import sqlite3
import json
import os
import string
print(os.getcwd())

conn = sqlite3.connect('banking_api/bankingapi.db')

cursor = conn.cursor()

# delete all rows from all three tables
cursor.execute("DELETE FROM 'transaction';")
cursor.execute("DELETE FROM account;")
cursor.execute("DELETE FROM customer;")
conn.commit()

# initialise with given json
json_obj = json.load(open('data/customers.json'))
print(json_obj)

alphabet = list(string.ascii_lowercase)

for i, row in enumerate(json_obj):

    sql = """INSERT INTO customer (name, identification)
          VALUES (?, ?)"""

    params = (row['name'], alphabet[i] * 5)

    cursor.execute(sql, params)

    conn.commit()

    print(row['name'], alphabet[i] * 5)


conn.close()

print('Database initialised with data')
