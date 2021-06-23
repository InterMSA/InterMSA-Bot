import sqlite3 as sql
import pandas as pd
from put import populate_links
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from tools import *

db_path = "database/database.db"
conn = sql.connect(db_path)

def sqlite_query(query, args=(), one=False):
   cur = conn.cursor()
   cur = conn.execute(query, args); conn.commit()
   rv = [dict((cur.description[idx][0], value)
              for idx, value in enumerate(row)) for row in cur.fetchall()]
   return (rv[0] if rv else None) if one else rv

def show_columns(table):
   cur = conn.cursor()
   query = f"PRAGMA table_info('{table}')"
   cur.execute(query); conn.commit()
   rows = cur.fetchall(); cols = ["| Field\t| Type\t\t| Null\t| Key\t| Default |", "+-------------------------------------------------+"]
   for row in rows:
      c_name = row[1][:7]
      c_type = row[2]
      if len(c_type) < 7:
         c_type = row[2] + "      "
      col = f"{c_name}\t| {c_type}\t| {row[3]}\t| {row[5]}\t| {row[4]}"
      cols.append(col)
   return cols

def show_data(table):
   print(f"{table} TABLE")
   records = 0
   for row in sqlite_query(f"SELECT * FROM {table}"):
      if records <= 10:
         print(row)
      records += 1
   if records == 0:
      print("Empty Table (no records)")
   else:
      print("Showing", records ,"total records")
   print("\n__________")

'''CREATE'''
##query = "CREATE TABLE Links(sid VARCHAR(40) PRIMARY KEY NOT NULL,"\
##        "full_name VARBINARY(130) NOT NULL, email VARBINARY(130) NOT NULL)"
##conn.execute(query)

'''CREATE MSU TABLE'''
##query = "CREATE TABLE MSU_Links(sid VARCHAR(40) PRIMARY KEY NOT NULL,"\
##        "full_name VARBINARY(130) NOT NULL, email VARBINARY(130) NOT NULL)"
##conn.execute(query)

'''RENAME LINKS TABLE TO NJIT_LINK'''
##query = "ALTER TABLE Links RENAME TO NJIT_Links"
##conn.execute(query)

'''INSERT'''
##populate_links(conn, "loot.txt")
##sid = hashlib.sha1("djm65".encode()).hexdigest()
##name = encrypt("David Jake Morfe")
##email = encrypt("djm65@njit.edu")
##query = "INSERT INTO Links(sid, full_name, email) VALUES(?,?,?)"
##sqlite_query(query, (sid, name, email))

'''INSERT CHECK'''
##query = "SELECT * FROM Links WHERE sid=?"
##result = sqlite_query(query, (sid,), one=True)
##print("Decrypted Result:", decrypt(result["full_name"]))

'''UPDATE'''
##query = "UPDATE Users SET EIN='850361090' WHERE user='abc123'"
##conn.execute(query)
##print("Record updated!")

'''DELETE'''
##sqlite_query("DELETE FROM Links WHERE sid=?", ('3',))
##print("Record deleted!")
##sqlite_query("DELETE FROM Links")
##print("Table data deleted!")

'''DROP'''
##sqlite_query("DROP TABLE Links")
##print("Table deleted!")

'''SELECT'''
show_data("Links")

'''SHOW COLUMNS'''
for column in show_columns('Links'):
   print(column)

conn.close()
