# this file is to just access other files from other directories.


import os,re
CWD = os.getcwd(); ENV = "(PROD GCE)"

# cwd = os.getcwd() 

DB_PATH = "database/database.db"

try: #goes into the folder of secret
    os.chdir("secrets") #we access the folder named 'secrets' that has the passwords 
except FileNotFoundError:
    pass

# print (os.getcwd()) #for debugging purpuses
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
      
def famous():
    try: 
        os.chdir("FAQ")  
    except FileNotFoundError:
        pass

    with open("famous_events.md") as f:
        return f.read()

# def commands():
#     os.chdir("FAQ")
#     with open("cmds.md") as f:
#         return f.read()

def mod_commands():
    try: 
        os.chdir("FAQ")  
    except FileNotFoundError:
        pass
    with open("cmds_for_mods.md") as f:
        return f.read()

def volunteer():
    try: 
        os.chdir("FAQ")  
    except FileNotFoundError:
        pass

    with open("volunteer.md") as f:
        return f.read()


def com():
    try: 
        os.chdir("FAQ")  
    except FileNotFoundError:
        pass

    with open("cmds_for_mods.md") as f:
        return f.read()

# def bot_pass():
#     with open("bot.txt") as f:
#         return f.read()