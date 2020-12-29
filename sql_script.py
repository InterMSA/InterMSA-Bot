import sqlite3 as sql
import pandas as pd
from put import populate_links


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
      print(row)
      records += 1
      if records == 10: break # Stop short
   if records == 0:
      print("Empty Table (no records)")
   else:
      print("Showing", records ,"total records")
   print("\n__________")

'''CREATE'''
##query = "CREATE TABLE Links(sid VARCHAR(32) PRIMARY KEY NOT NULL,"\
##        "full_name VARCHAR(64) NOT NULL, email VARCHAR(32) NOT NULL)"
##conn.execute(query)

'''INSERT'''
##populate_links(conn, "loot.txt")
##query = "INSERT INTO Links(sid, full_name, email) VALUES(?,?,?)"
##sqlite_query(query, ("djm65", "David Jake Morfe", "djm65@njit.edu"))

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
