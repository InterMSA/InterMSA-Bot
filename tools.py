import asyncio
import re, os, time, smtplib
import sqlite3 as sql
from random import randint
from email.message import EmailMessage
from config import *
# (Note: All variables not declared probably came from config.py)


#If email treated as spam:
 #https://support.google.com/mail/contact/bulk_send_new?rd=1
#Print Emojis Safely
 #print(u'\U0001f604'.encode('unicode-escape'))
 #print('\N{grinning face with smiling eyes}')
#Make way to update #role-selection


DB_CONN = sql.connect(DB_PATH)


# Remove a line from a file based on value
def edit_file(file, value):
    with open(file, 'r+') as f:
        lines = f.readlines()
        f.seek(0); found = False
        for line in lines:
            line = line.strip('\n')
            if str(line).lower() != str(value).lower():
                f.write(line + '\n')
            else:
                found = True
        f.truncate()
        return found

# Return 4-digit verification code string after sending email
def send_email(addr: str, test=False) -> str:
    sCode = f"{randint(0,9)}{randint(0,9)}{randint(0,9)}{randint(0,9)}"
    if not test:
        msg = EmailMessage()
        msg.set_content(f"\
    <html><body><b>Your verification code to join the chat is below:<br><br>\
    <h2>{sCode}</h2></b>Please copy & paste this code in the \
    <i><u>#verify</u></i> text channel of your InterMSA Discord. \
    This code will expire in 15 minutes.</body></html>", subtype="html")
        msg["Subject"] = "Verification Code for InterMSA Discord"
        msg["From"] = "noreply.njitmsa@gmail.com"
        msg["To"] = addr
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
                s.login("noreply.njitmsa@gmail.com", APP_PASS)
                s.send_message(msg)
    else:
        print(sCode)
    return sCode

# SQL Query Function
def sqlite_query(query, args=(), one=False):
   cur = DB_CONN.cursor()
   cur = DB_CONN.execute(query, args); DB_CONN.commit()
   rv = [dict((cur.description[idx][0], value)
              for idx, value in enumerate(row)) for row in cur.fetchall()]
   return (rv[0] if rv else None) if one else rv

# Return full name string based on email
def get_name(addr: str) -> str:
    sid = re.sub(r"@.+\.", '', str(addr))
    sid = sid.replace("edu", '')
    query = f"SELECT full_name FROM Links WHERE sid='{sid}'"
    result = sqlite_query(query, one=True)
    if result != None:
        return str(result["full_name"])

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

# Retrieve role for those in waiting room
def get_sibling_role(member):
    roles = member.roles; ret = None
    for role in roles:
        if role.name == "Brothers Waiting Room":
            ret = ("Brother", role); break
        elif role.name == "Sisters Waiting Room":
            ret = ("Sister", role); break
        elif role.name == "Pros Waiting Room":
            ret = ("Professional", role); break
    return ret

# Return sibling global object based on gender
def get_sibling(sibling):
    if sibling == "Brother":
        return BROTHERS
    elif sibling == "Sister":
        return SISTERS
    else:
        return PROS

# Return announcement channel id while listening to announcements
def listen_announce(msg):
    if msg.channel.id == BROTHERS.announce:
        if "@everyone" in msg.content:
            return SISTERS.announce
    elif msg.channel.id == SISTERS.announce:
        if "@everyone" in msg.content:
            return BROTHERS.announce
    else:
        False

# Return role based on emoji
def listen_role_reaction(emoji):
    role_id = 0
    emoji = emoji.name.encode('unicode-escape')
    emote = re.search(r".+?\\", str(emoji).strip("b'\\"))
    if emote and str(emoji).lower().count('u') > 1:
        emoji = ("\\" + emote.group().strip('\\')).encode()
    for role_emoji in ROLE_EMOJIS:
        if emoji == role_emoji.encode('unicode-escape'):
            return ROLE_EMOJIS[role_emoji]
    return False

# Parse and return email & join type based on /verify request
def listen_verify(msg):
    if msg.channel.id == VERIFY_ID:
        if msg.content.startswith('/verify'):
            request = re.sub(r"/verify ", '', msg.content)
            join_type = re.search(r"(brothers?|sis(tas?|ters?)|workforce)", request) or ''
            if join_type:
                email = re.sub(fr"{join_type.group()}", '', request).strip(' ')
                if join_type.group()[0] == 'b':
                    join_type = "Brother"
                elif join_type.group()[0] == 's':
                    join_type = "Sister"
                else:
                    join_type = "Professional"
                return email, join_type
            return ('', '')

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
