from key import *


class Server(object):
   #__slots__ = ("name", "wait", "general", "announce")
   def __init__(self, name, wait, general, announce, **kwargs):
      self.__dict__.update(kwargs)
      self.name = name
      self.wait = wait
      self.general = general
      self.announce = announce

class StaticMsg(object):
   __slots__ = ("channel", "message", "reaction")
   def __init__(self, channel, message, reaction):
      self.channel = channel
      self.message = message
      self.reaction = reaction

__bro_add_ons = {"role_select": 792531850740498482}
__sis_add_ons = {"role_select": 792531967832227841}

role_selection_s = role_selection_b = None
def set_role_selections():
   role_selection_s = (SISTERS.role_select, [StaticMsg(SISTERS.role_select,
                            "**Peer Mentee** :woman_with_headscarf:",
                            "\U0001f9d5"),
                  StaticMsg(SISTERS.role_select,
                            "**Senior** :older_woman:",
                            "\N{OLDER WOMAN}"),
                  StaticMsg(SISTERS.role_select,
                            "**Junior** :woman:",
                            "\N{WOMAN}"),
                  StaticMsg(SISTERS.role_select,
                            "**Sophmore** :girl:",
                            "\N{GIRL}"),
                  StaticMsg(SISTERS.role_select,
                            "**Freshmen** :baby:",
                            "\N{BABY}"),
                  StaticMsg(BROTHERS.role_select,
                            "**MATH Review** :straight_ruler:",
                            "\N{STRAIGHT RULER}"),
                  StaticMsg(BROTHERS.role_select,
                            "**CS Review** :computer:",
                            "\N{DESKTOP COMPUTER}"),
                  StaticMsg(BROTHERS.role_select,
                            "**PHYS Review** :atom:",
                            "\N{ATOM SYMBOL}"),
                  StaticMsg(BROTHERS.role_select,
                            "**CHEM Review** :test_tube:",
                            "\N{TEST TUBE}")])
   role_selection_b = (BROTHERS.role_select, [StaticMsg(BROTHERS.role_select,
                            "**MATH Review** :straight_ruler:",
                            "\N{STRAIGHT RULER}"),
		          StaticMsg(BROTHERS.role_select,
                            "**CS Review** :computer:",
                            "\N{DESKTOP COMPUTER}"),
                  StaticMsg(BROTHERS.role_select,
                            "**PHYS Review** :atom:",
                            "\N{ATOM SYMBOL}"),
                  StaticMsg(BROTHERS.role_select,
                            "**CHEM Review** :test_tube:",
                            "\N{TEST TUBE}"),
                  StaticMsg(BROTHERS.role_select,
                            "**Quran Circle** :book:",
                            "\N{OPEN BOOK}")])

# Set all global variables
BROTHERS = Server("Brother", 791466388031668265,
                  791468944786980904, 791468851724419142,
                  **__bro_add_ons)
SISTERS = Server("Sister", 791466441031417866,
                 791468979591315476, 791468879067086848,
                 **__sis_add_ons)
##set_role_selections(); CONST_MSG = [role_selection_s, role_selection_b] # To be deprecated
BOT = os.getenv("BOT_SECRET", bot_pass())
DB_SECRET = os.getenv("DB_SECRET", db_pass())
APP_PASS = os.getenv("EMAIL_SECRET", email_pass())
DB_PATH = "database/database.db"
VERIFY_ID = 791466283836506162
SERVER_ID = 777022217284354079
COLLEGES = {"njit": 793236123124105227, "rutgers": 793236159027085372,
            "montclair": 793236379722842113, "fdu": 793236409816317982,
            "ramapo": 793236446789369926, "shu": 793236471259201607,
            "stevens": 793236525302939658, "tcnj": 793236740457627668,
            "stockton": 793236769415364648}
ROLE_EMOJIS = {"\U0001f9d5": 750931950964965506,
               "\N{STRAIGHT RULER}": 756328774764593173,
               "\N{DESKTOP COMPUTER}": 756329639588397197,
               "\N{ATOM SYMBOL}": 756334778881540137,
               "\N{TEST TUBE}": 756335021933068288,
               "\N{OPEN BOOK}": 762052942302937111,
               "\U0001f4f6": 783048947291258920,
               "\U0001f9a0": 783049863243104296,
               "\U0001f9be": 783050320552001587,
               "\U0001f3d7": 783050450462703616,
               "\U0001f4af": 778401907713638460}
os.chdir(CWD) # Return to original directory


'''
Notes:
- Create 'Sibling' role or w/e you wanna call the role that
  every sister gets to officially join
- Create #verify chat
- Enable Developer Mode
  Copy ID's:
  - Right click on Server Name
  - Right click on #verify chat
  - Right click on #general chat
- Make @everyone role only able to talk in #verify chat
'''
