import os,re
CWD = os.getcwd(); ENV = "(PROD GCE)"

# cwd = os.getcwd()
#os.chdir("..");os.chdir("..");os.chdir("..")
#os.chdir("Desktop\\Prog\\CaliBot")
DB_PATH = "database/database.db"

try: #goes into the folder of secret
    os.chdir("secret")
except FileNotFoundError:
    pass
#print (os.getcwd())
def bot_pass():
    with open("bot.txt") as f:
        return f.read()

def db_pass():
   try:
      with open("private.txt") as f:
         #privatekey = f.read()
         return f.read()
   except FileNotFoundError:
      pass

def pub_pass():
   try:
      with open("public.txt") as f:
         return f.read()
   except FileNotFoundError:
      pass

    
def secret_pass():
   try:
      with open("sp.txt") as f:
         return f.read()
   except FileNotFoundError:
      pass
def db_pass():
    with open("db.txt") as f:
        return f.read()
DB_SECRET = re.sub(r"\\n", '\n', os.getenv("DB_SECRET", db_pass()))

def email_pass():
    with open("email.txt") as f:
        return f.read()
