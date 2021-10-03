import re
from key import *


# Object for representing a partition in a server
class ServerPartition(object):
   #__slots__ = ("name", "wait", "general", "announce")
   def __init__(self, name, wait, general, announce, **kwargs):
      self.__dict__.update(kwargs)
      self.name = name
      self.wait = wait
      self.general = general
      self.announce = announce

# Update the role-selection listener
def update_uni_library():
   with open("uni_library.txt", encoding="utf-8") as f:
      lines = f.readlines()
      for line in lines:
         uni, role = line.split(' ')
         if uni not in COLLEGES:
            COLLEGES[uni] = int(role)

# Update the role-selection listener
def update_role_select():
   with open("role_selection.txt", encoding="utf-8") as f:
      lines = f.readlines()
      for line in lines:
         extra, emote, role = line.split(' ')
         if extra == '0' and emote not in ROLE_EMOJIS:
            ROLE_EMOJIS[emote] = int(role)
         elif extra != '0' and \
              emote not in SPLIT_ROLES_EMOJIS[BROTHERS.role_select] or \
              emote not in SPLIT_ROLES_EMOJIS[SISTERS.role_select]:
            SPLIT_ROLES_EMOJIS[BROTHERS.role_select][emote] = int(role)
            SPLIT_ROLES_EMOJIS[SISTERS.role_select][emote] = int(extra)


# Attributes to add on to ServerPartition object(s)
__bro_add_ons = {"role_select": 792531850740498482,
                 "events": 811467259225702480}
__sis_add_ons = {"role_select": 792531967832227841,
                 "events": 811471035332296740}
__pro_add_ons = {"role_select": 793371378736431144}

# Set all global variables
# PROS, BROTHERS & SISTERS represent the server partitions
BROTHERS = ServerPartition("Brother", 791466388031668265,
                  791468944786980904, 791468851724419142,
                  **__bro_add_ons)
SISTERS = ServerPartition("Sister", 791466441031417866,
                 791468979591315476, 791468879067086848,
                 **__sis_add_ons)
PROS = ServerPartition("Pro", 792530124560924677,
                  792531673371246612, 793371080864563200,
                  **__pro_add_ons)

           #"join
# Retrieve passwords/secrets
BOT = os.getenv("BOT_SECRET", bot_pass())
VERIFY_SITE = "https://VerificationSystem.intermsa.repl.co"
SP = os.getenv("SECRET_PASS", secret_pass())
DB_SECRET = re.sub(r"\\n", '\n', os.getenv("DB_SECRET", db_pass()))
#ENCRYPT_KEY = re.sub(r"\\n", '\n', os.getenv("PUBLIC_KEY", pub_pass()))
APP_PASS = os.getenv("EMAIL_SECRET", email_pass())
DB_PATH = "database/database.db"

# Needed ID's
VERIFY_ID = 791466283836506162 # #verify chat channel
SERVER_ID = 777022217284354079 # Server ID

# Library of colleges under InterMSA
COLLEGES = {"njit": 793236123124105227, "rutgers": 793236159027085372,
            "montclair": 793236379722842113, "fdu": 793236409816317982,
            "ramapo": 793236446789369926, "shu": 793236471259201607,
            "stevens": 793236525302939658, "tcnj": 793236740457627668,
            "stockton": 793236769415364648, "njcu": 797974411906514956,
            "pccc": 809924040587870250, "spu": 820882908372795392,
            "saintpeters": 820882908372795392, "kean": 832071978935517245,
            "mcdaniel": 836739387295399946}

# Libraries of role emojis accessible through #role-selection chat
ROLE_EMOJIS = {"\U0001f4af": 792530378719756318,
               "\U0001f50d": 793380988125970464,
               "\U0001f50c": 793381155021914124,
               "\U0001f9d4": 830450589841883176,
               "\U0001f9d5": 830450726982647818,
               "\U0001f4d6": 819249140771848213}
SPLIT_ROLES_EMOJIS = {BROTHERS.role_select:
                      {"\U0001f4e2": 811466169072222221,
                       "\U00002753": 819249562869956668,
                       "\U0001f5f3": 822259258690371614,
                       "\U0001f3ae": 826886828665470996,
                       "\U0001f4f7": 826890240533856286},
                      SISTERS.role_select:
                      {"\U0001f4e2": 811470807033315359,
                       "\U00002753": 819249898334453801,
                       "\U0001f5f3": 822259456619708500,
                       "\U0001f3ae": 826886911339266089,
                       "\U0001f4f7": 826890322700271676},
                      PROS.role_select: {}}

# Last globals and config setup
DEVS = [233691753922691072, 714641624571052076, 670325339263860758,
        508654889002467329, 714618776020320396, 459493208905220138,
        732373611775524926, 562285596668723219]
#COMMAND_PREFIX = '/'
COMMAND_PREFIX =["/",">"]
#bot = commands.Bot(command_prefix=["hi ","Hi "])
TEST_MODE = False; MSA = "InterMSA"; ENV = ENV
os.chdir(CWD) # Return to original directory
update_uni_library() # Update the COLLEGE library upon startup
update_role_select() # Update the role-selection listener upon startup

'''
Notes:
- Create Server
- Create Brother/Sister, Owner, Waiting oom roles role
- Create #verify chat
- Create waiting rooms
- Create Bro/Sis Categories
- Set Perms
- Enable Developer Mode
  Copy ID's:
  - Right click on Server Name
  - Right click on #verify chat
  - Right click on #general chats for brothers & sisters
- Make @everyone role only able to talk in #verify chat
- Remove all permissions from @everyone role except for send messages
'''
