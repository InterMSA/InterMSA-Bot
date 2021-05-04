import os

CWD = os.getcwd(); ENV = "DEV"
try:
    os.chdir(".."); os.chdir(".."); os.chdir("..")
    os.chdir("Desktop\\Prog\\InterMSA-Bot")
except FileNotFoundError:
    pass

try:
    os.chdir("secret")
except FileNotFoundError:
    pass

def bot_pass():
   try:
      with open("bot.txt") as f:
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
   try:
      with open("db.txt") as f:
         return f.read()
   except FileNotFoundError:
      pass

def pub_pass():
   try:
      with open("pub.txt") as f:
         return f.read()
   except FileNotFoundError:
      pass

def email_pass():
   try:
      with open("email.txt") as f:
         return f.read()
   except FileNotFoundError:
      pass
