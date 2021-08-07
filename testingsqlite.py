import sqlite3
import sys
import datetime
#from datetime import datetime
#from datetime import timedelta
from dateutil import parser

sys.path.append('..')
db = sqlite3.connect('time.sqlite')
cursor = db.cursor()

cursor.execute('''
	CREATE TABLE IF NOT EXISTS zam_time (
	
		guild_id text NOT NULL, 
		user_id text NOT NULL, 
		content text, 
		created timestamp without time zone, 
		expired timestamp without time zone, 
		completed boolean Default 0, 
		row_id integer PRIMARY KEY, 
		channel_id text NOT NULL, url text NOT NULL)''') 

db = sqlite3.connect('time.sqlite')
cursor = db.cursor()

#my_data = ("user_ID","guild_id",now,now,"sentence","us/st/.com","channel_id",True)
#my_query=('''
#            INSERT INTO za_time(user_id,guild_id, created, expired,content,url,channel_id,completed) VALUES(?,?,?,?,?,?,?,?)
#        ''')

#cursor.execute('SELECT * FROM zam_time WHERE NOT completed ORDER BY expired')
#status = cursor.fetchone()

_id=(99)
user_ID = ("670325339263860758")


my_query=(f'''DELETE from zam_time WHERE row_id={_id} AND user_id = {user_ID} ''')
status=db.execute(my_query)
db.commit()

print(status)
if next_task == None:
	print("its empty bruh")
#else:
#	print("DELETEed")

#cursor.close()
#db.close()

now=datetime.datetime.now()

#q="SELECT * from za_time"

#my_data=(1)
query=cursor.execute(f'SELECT * FROM zam_time ORDER BY expired limit 10 ')
records = cursor.fetchall()
#print (records)
#my_cursor=db.execute(next_task)

#yay = "2021-08-05 04:38:04.164445"
#print("yay is ",yay)
#yay = parser.parse(yay)
#date = datetime.datetime.strptime(next_task[4], '%Y-%m-%d %H:%M:%S.%f')
#2021-08-05 04:38:04.164445
#date = datetime.datetime.strptime(yay, '%Y-%m-%d %H:%M:%S')
#if (yay) >= now:
#print(next_task)
#print(records,"\n")
#for row in records:
#	print (row[6])

#row = ()
    #print(row[0],"\n",row[1],"\n",row[2],"\n",
    #	row[3],"\n",row[4])

#for key,value in dict_example.items():
#    print(key + " : " + str(value))
#print (dict_example)