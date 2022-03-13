import asyncio, aiohttp
import re, os, time, smtplib, hashlib
import sqlite3 as sql
from random import randint
from email.message import EmailMessage
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from config import *
from key import *

from flask import Flask, render_template


try:
    import GeoLiberator as GeoLib
except ModuleNotFoundError:
    pass
# (Note: All variables not declared probably came from config.py)

#If email treated as spam:
 #https://support.google.com/mail/contact/bulk_send_new?rd=1


DB_CONN = sql.connect(DB_PATH)
KEY = RSA.import_key(DB_SECRET.encode("ascii"), SP) # Just you try and get it :D

print (os.getcwd())
# print (os.listdir())

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

class words:
    code = 'http://google.com/'



# Return 4-digit verification code string after sending email with verification link
def send_email(addr: str, gender='', test=False) -> str: #takes email, the gender
    print(addr)
    print (gender)
    sCode = f"{randint(0,9)}{randint(0,9)}{randint(0,9)}{randint(0,9)}" #randome number of 4 digits, so it can make a unique link 
    verify_link = f"{VERIFY_SITE}/verified/{sCode}/{gender}" #here will generate a code that expires after particular time
    #example: https://VerificationSystem.intermsa.repl.co/verified/1460/Brother

    verify_btn = f'<a class="button" type="button" href="{verify_link}" target="_blank">VERIFY!</a>'

# Start of old code 
    # style_btn = """<head><style>
    #                 .button {
    #                     font-size: 14px;
    #                     text-decoration: none;
    #                     background-color:#0BA2D3;
    #                     color: #FFFFFF;
    #                     border-radius: 2px;
    #                     border: 1px solid #0A83A8;
    #                     font-family: Helvetica, Arial, sans-serif;
    #                     font-weight: bold;
    #                     padding: 8px 12px;
    #                 }
    #                 .button:hover {
    #                     background-color:#0FC7FF
    #                 }
    #               </style></head>"""
    
     

    # index = open("index.html").read().format(first_header='goodbye')
    # html = html.format(verify_link)
    
    # message.format(URL))

    # html = f"""<html>{style_btn}<body>
    #         <b>Your verification link to join the chat is below:<b><br><br>
    #         <a class="button" type="button" href="{verify_link}" target="_blank">VERIFY!</a><br>
    #         <h4>{verify_link}</h4><br>
    #         Please click this link to join the InterMSA Discord. This link will expire in 15 minutes.
    #         </body></html>"""

# end of old code
# ----------------------------------- 

    os.chdir("./template") # cd template
    html = open("file.html").read()
    #.format(p=words())
    
    if not test:
        msg = EmailMessage()
        # msg.set_content(html, subtype="html")
        msg.set_content(html,subtype="html")

        msg["Subject"] = "Verification Link for InterMSA Discord"
        msg["From"] = "no-reply@intermsa.com"
        msg["To"] = addr
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
                s.login("intermsa.discord@gmail.com",
                        APP_PASS)
                s.send_message(msg)
    
    # app = Flask(__name__)
    app = Flask(__name__, template_folder='template')

    @app.route('/') #I added this in hopes to test case the template and render it on python instead of sending emails everytime, it did not work with me yet
    def home(): 
       return render_template(html)
    if __name__ == '__main__':
       app.run()

    else:
        print(verify_link)
    return sCode

# send_email('nassarb1@montclair.edu','Brother') #this is for test cases, change Baraa's email to your emails plz when testing


# SQL Query Function
def sqlite_query(query, args=(), one=False):
   cur = DB_CONN.cursor()
   cur = DB_CONN.execute(query, args); DB_CONN.commit()
   rv = [dict((cur.description[idx][0], value)
              for idx, value in enumerate(row)) for row in cur.fetchall()]
   return (rv[0] if rv else None) if one else rv

def encrypt(msg):
    cipher = PKCS1_OAEP.new(KEY.publickey())
    cipher_text = cipher.encrypt(msg.encode())
    return cipher_text

def decrypt(cipher_text):
    cipher = PKCS1_OAEP.new(KEY)
    decrypted_text = cipher.decrypt(cipher_text)
    return decrypted_text.decode()

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

#sibling = get_sibling_role(member)

# Return announcement channel id while listening to announcements/events
def listen_announce(msg):
    if msg.channel.id == BROTHERS.announce:
        if "@everyone" in msg.content:
            return SISTERS.announce
    elif msg.channel.id == SISTERS.announce:
        if "@everyone" in msg.content:
            return BROTHERS.announce
    elif msg.channel.id == BROTHERS.events:
        if "@everyone" in msg.content:
            return SISTERS.events
    elif msg.channel.id == SISTERS.events:
        if "@everyone" in msg.content:
            return BROTHERS.events
    else:
        False

# Return role id based on emoji
def listen_role_reaction(emoji, channel):
    role_id = 0
    emoji = emoji.name.encode('unicode-escape')
    emote = re.search(r".+?\\", str(emoji).strip("b'\\"))
    if emote and str(emoji).lower().count('u') > 1:
        emoji = ("\\" + emote.group().strip('\\')).encode('unicode-escape')
    for role_emoji in ROLE_EMOJIS:
        if "\\U" not in emoji.decode():
            if emoji.decode() in role_emoji:
                return ROLE_EMOJIS[role_emoji]
        if emoji == role_emoji.encode('unicode-escape'):
            return ROLE_EMOJIS[role_emoji]
    if len(emoji) == 11:
        emoji = emoji[1:].decode('unicode-escape')
    else:
        emoji = emoji.decode('unicode-escape')
    for role_select_channel in SPLIT_ROLES_EMOJIS:
        if role_select_channel == channel:
            return SPLIT_ROLES_EMOJIS[channel][emoji]
    return role_id

# Parse and return email & join type based on /verify request
def listen_verify(msg):
    if msg.channel.id == VERIFY_ID or msg.channel.id == 814602442910072842:
        if msg.content.startswith(f'{COMMAND_PREFIX[0]}verify') or "@" in msg.content:
            request = re.sub(fr"{COMMAND_PREFIX[0]}verify ", '', msg.content.lower())
            join_type = re.search(r"(bro(ther)?s?|sis(tas?|ters?)|work(force)?)", request) or ''
            if join_type:
                email = re.sub(fr"{join_type.group()}", '', request).strip(' ')
                if join_type.group()[0] == 'b':
                    join_type = "Brother"
                elif join_type.group()[0] == 's':
                    join_type = "Sister"
                elif join_type.group()[0] == 'w':
                    join_type = "Professional"
                else:
                    join_type = ''
                return email, join_type
            return (request, '')
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
