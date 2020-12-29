import re, time, sqlite3
from config import DB_SECRET

def populate_links(conn, data_file):
   cur = conn.cursor()
   to_db = []
   with open(data_file) as f:
      line = f.readline(); c = 0; thous = '0'
      while line.strip('\n') != '':
         try:
            line = f.readline(); line = line.strip('\n')
         except UnicodeDecodeError:
            with open("bad.txt", 'a') as w:
               w.write(line + '\n')
            continue
         if line == '':
            break
         lst = line.split('\t')
         try:
            ucid = re.sub(r"@.+\.edu", '', lst[1])
            email = lst[1]
            names = lst[0].split(',')
         except IndexError: # Ignore non-person records
            print("False record dodged!", lst)
            continue

         if len(names) == 2:
            name = names[-1] + ' ' + names[0]
         elif len(names) == 3:
            if len(names[2]) != 1:
               name = names[-1] + ' ' + names[1] + ' ' + names[0]
            else:
               name = name[1] + ' ' + name[-1] + ' ' + names[0]
         else:
            name = names[0]
         name = re.sub(r"  ", ' ', name).strip(' ')

         if len(ucid) > 8 or len(name) > 55 or len(email) > 20: # Ignore professor records
            continue
         # Encrypt here (32 B, 64 B, 32 B)
         # RSA Algorithm
         val = (ucid, name, email)
         to_db.append(val); c += 1
         if str(c)[0] != thous:
            thous = str(c)[0]
            print("Number of appended records:", c)

   query = "INSERT INTO Links VALUES(?,?,?)"
   cur.executemany(query, to_db)
   conn.commit()
   print("\nDone!\n", c, "records created!")
   print("Database updated!")
