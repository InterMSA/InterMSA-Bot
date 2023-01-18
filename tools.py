import asyncio, aiohttp
import re, os, time, smtplib, hashlib
import sqlite3 as sql
from random import randint
from email.message import EmailMessage
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from config import *
from key import *
from discord.utils import get
# DB_CONN = sql.connect(DB_PATH)
# KEY = RSA.import_key(DB_SECRET.encode("ascii"), SP) # Just you try and get it :D

# Remove a line from a file based on value
def edit_file(file, value, exact=True):
    with open(file, 'r+', encoding="utf-8") as f:
        lines = f.readlines()
        f.seek(0); found = False
        if exact == True:
            for line in lines:
                line = line.strip('\n')
                if str(line).lower() != str(value).lower():
                    f.write(line + '\n')
                else:
                    found = True
        else:
            for line in lines:
                line = line.strip('\n')
                if str(value).lower() not in str(line).lower() :
                    f.write(line + '\n')
                else:
                    found = True
        f.truncate()
        return found

# Return 4-digit verification code string after sending email with verification link

# SQL Query Function
# Return full name string based on email

def get_name(addr: str) -> str:
    if "njit" not in addr and "montclair" not in addr:
        return None
    sid = re.sub(r"@.+\.", '', str(addr))
    sid = sid.replace("edu", '')
    hashed_sid = hashlib.sha1(sid.encode()).hexdigest()
    school = re.search(r"\w+(?=\.edu)", addr).group()
    if school.lower() == "montclair":
        school = "msu"
    table_name = school.upper() + "_Links"
    query = f"SELECT full_name FROM {table_name} WHERE sid=?"
    result = sqlite_query(query, (hashed_sid,), one=True)
    if result != None:
        full_name = result["full_name"]
        return decrypt(full_name)

# Return gender based on user
def check_gender(user):
    roles = user.roles
    for role in roles:
        if role.name == "Brother" or role.name == "Sister":
            return role.name

# Return true if user is admin or another role
def check_admin(msg, add_on=''):
    roles = msg.author.roles
    for role in roles:
        if role.name == "Admin" or "Shura" in role.name:
            return True
        if role.name == add_on:
            return True
    return False

greeting=["WELCOME WELCOME! ",f"*has* ***officially*** *joined the InterMSA Discord! Welcome!", "just hopped in! say Salam ",
          "REVEAL YOUR IDENTITY ... welcome :) ", "5 dollars upon entry ... Welcome aboard 🛬 ",
           "welcome aboard ", "You have reached your destination ","ASALAM ALAYKUM! welcome ", "did you knock the door? welcome to interMSA "
           ,"Just joined, SALAAM! "]

# Retrieve role for those in waiting room
def get_sibling_role(member):
    roles = member.roles; ret = None
    # for role in roles:

    # if (role.name == "Brothers Waiting Room") in member.roles:
    if get(roles, name = "Brothers Waiting Room"):#if the id is Brothers Waiting Room
        # print ("hi")
        ret = ("Brother"); 

    if get(roles, name = "Sisters Waiting Room"):#if the id is Brothers Waiting Room
        ret = ("Sister"); 

    if get(roles, name = "Pros Waiting Room"):#if the id is Brothers Waiting Room
        ret = ("Professional", role); 
    return ret

# bot = Bot()
# guild = bot.get_guild(SERVER_ID)
# # member = guild.get_member(int(761123575021174784))
# print (guild)


# Return sibling global object based on gender
def get_sibling(sibling):
    if sibling.lower() == "brother" or sibling.lower() == "male" or sibling.startswith("bro"):
        return BROTHERS
    elif sibling.lower() == "sister" or sibling.lower() == "female" or  sibling.startswith("sis"):
        return SISTERS
    else:
        return None


#sibling = get_sibling_role(member)

# Return announcement channel id while listening to announcements/events

def listen_announce(msg): #1025948580575457310 == @InterMSA Event Notifications
    if msg.channel.id == BROTHERS.announce: 
        if ("<@&1025948580575457310>" in msg.content) or (("@everyone" in msg.content)):
            return SISTERS.announce
    elif msg.channel.id == SISTERS.announce:
        if ("<@&1025948580575457310>" in msg.content) or (("@everyone" in msg.content)):
            return BROTHERS.announce
    elif msg.channel.id == BROTHERS.events:
        if ("<@&1025948580575457310>" in msg.content) or (("@everyone" in msg.content)):
            return SISTERS.events
    elif msg.channel.id == SISTERS.events:
        if ("<@&1025948580575457310>" in msg.content) or (("@everyone" in msg.content)):
            return BROTHERS.events
    else:
        False

# Listen for 4-digit code in #verify
def listen_code(msg):
    if msg.channel.id == VERIFY_ID:
        return re.search(r"^\d\d\d\d$", msg.content)

# Return sibling global object based on general channel_id
def in_general(channel_id):
    if channel_id == BROTHERS.general:
        return BROTHERS
    elif channel_id == SISTERS.general:
        return SISTERS
    else:
        return False

# Send Post Request
async def send_verify_post(data={}, test=False):
    if test:
        return '1'
    url = VERIFY_SITE + '/verify'
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as resp:
            result = await resp.text()
    return result

# Dynamically mute/unmute every member in a voice channel
async def mute_voice_members(voice_channel, mute=True):
    for member in voice_channel.members:
        await member.edit(mute=mute)

# Constantly check for changes in verify.txt
async def check_verify(record, msg, temp):
    while True:
        with open("verify.txt") as f:
            text = f.read()
            if not re.search(fr"{record}", text):
                break
        await asyncio.sleep(0)
    await msg.delete(); await temp.delete()
