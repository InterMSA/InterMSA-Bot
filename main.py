# -*- coding: utf-8 -*-
'''
Author: David J. Morfe
Application Name: InterMSA-Bot
Functionality Purpose: An agile Discord Bot to fit InterMSA's needs
'''
RELEASE = "v0.2.0 - 12/30/20"


import re, os, sys, time, json, datetime
from cmds import *
from config import *
from tools import *
try:
    import GeoLiberator as GL
except ModuleNotFoundError:
    pass
RUN_TIME = datetime.datetime.now()
LAST_MODIFIED = RUN_TIME.strftime("%m/%d/%Y %I:%M %p")


class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
    def writelines(self, datas):
        self.stream.writelines(datas)
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self .stream, attr)
sys.stdout = Unbuffered(sys.stdout)

# Executes when bot begins running
@bot.event
async def on_ready():
    await bot.change_presence(activity = Game(name = "/help (For all cmds)"))
    print("We have logged in as {0.user}".format(bot))

'''@bot.event
async def on_member_join(member):
    #await bot.edit_message(message_var, "This is the edit to replace the message.")
    channel = bot.get_channel(BROTHERS.general)
    await asyncio.sleep(15)
    await channel.send("__***Welcome to the NJIT MSA Discord Server!***__\n\n**Please type `/verify <YOUR_NJIT_UCID>` to join the chat.**")'''

# Listen to added reactions in specified channels
@bot.event
async def on_raw_reaction_add(payload):
    if payload.channel_id != SISTERS.role_select and \
       payload.channel_id != BROTHERS.role_select and \
       payload.channel_id != PROS.role_select:
        return -1
    role_id = listen_role_reaction(payload.emoji)
    if role_id:
        role = get(
                    bot.get_guild(SERVER_ID).roles, id=role_id)
        del(role_id)
        await payload.member.add_roles(role)

# Listen to removed reactions in specified channels
@bot.event
async def on_raw_reaction_remove(payload):
    if payload.channel_id != SISTERS.role_select and \
       payload.channel_id != BROTHERS.role_select and \
       payload.channel_id != PROS.role_select:
        return -1
    role_id = listen_role_reaction(payload.emoji)
    if role_id:
        guild = bot.get_guild(SERVER_ID)
        member = guild.get_member(payload.user_id)
        role = get(guild.roles, id=role_id)
        del(role_id); del(guild)
        try:
            await member.remove_roles(role)
        except AttributeError:
            return -1

# Standard InterMSA Bot Commands
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return -1;
    # Exclusive Experimental Commands
    if message.content == 'nu u':
        if "Cali#6919" == str(message.author):
            await message.channel.send("nu u!")
    if message.content.lower().startswith('/version'):
        if "Cali#6919" == str(message.author):
            await message.channel.send(f"`{RELEASE} | {LAST_MODIFIED}`")
    if re.search("(nu nu|Nunu|nunu)", message.content): # Taha
        if message.author.id == 496079190475538461:
            await message.channel.send("nu nu?")
    if "/taha" in message.content.lower(): # Taha
        if message.author.id == 496079190475538461:
            await message.channel.send("Yes we can")
    if "/anas" in message.content.lower(): # Anas
        if message.author.id == 406821958563528737:
            await message.channel.send("knowimsayin dawg", delete_after=10)
    if "Solo Leveling" in message.content:          
        if message.author.id == 185842527520292874: # Omar E.
            await message.channel.send("Yo that junk is fire :fire:", delete_after=10)
    if "ws" == message.content:
        await message.channel.send("Walaikumu Salam")
    if "texas" in str(message.content).lower(): # Siraj
        if message.author.id == 416430987241586698:
            await message.channel.send("https://media.tenor.co/videos/c8bad30e8d9834c6543b7575c3d7bd89/mp4")
    if "cap" in str(message.content).lower(): # Usmaan
        if message.author.id == 397082457179947029:
            await message.channel.send("yo that's cap'n cap'n")
    if "egg" in str(message.content).lower(): # Egg
        if message.author.id == 714641624571052076:
            await message.channel.send("Because I'm Eggcellent", delete_after=10)
            await asyncio.sleep(5)
            await message.channel.send("https://gyazo.com/8160eef16f1ae4c1c30add7044545542", delete_after=10)

    # Professional Introductions Chat
    if message.channel.id == PROS.wait:
        if not message.content.startswith("/add "):
            with open("introductions.txt", 'a') as f:
                user_id = str(message.author.id)
                msg_id = str(message.id)
                f.write(f"{user_id} {msg_id}\n")
            await message.delete(delay=600)

    # Shared Announcment System
    if listen_announce(message): # Send to alternate announcement channel
        announce_channel = listen_announce(message)
        channel = bot.get_channel(announce_channel)
        await channel.send(message.content)

    # Verification System
    if listen_verify(message): # Verify command
        email, gender = listen_verify(message)
        if not re.search(r"^\w+@\w+\.", email) or \
           not re.search(r"(Brother|Sister|Professional)", gender) or \
           not re.search(r"^/verify ", str(message.content)) or \
           email == '' and gender == '':
            await message.channel.send("**Invalid command! Please make sure you're typing everything correctly.**", delete_after=25)
            await message.delete(delay=300)
        elif re.search(r"\d{8}", message.content):
            await message.channel.send("**Invalid command! NOT your student ID, use your UCID!**", delete_after=25)
            await message.delete(delay=300)
        else:
            email_addr = email.lower()
            vCode = send_email(email_addr, test=True); ID = message.author.id
            with open("verify.txt", 'a') as f:
                f.write(f"{vCode} {email_addr} {ID} {gender}\n")
            temp = await message.channel.send(f"**We've sent a verification code to your email at** ___{email_addr}___**, please copy & paste it below.**", delete_after=300)
            await message.delete(delay=300)
            try: # Purge messages when record is removed from 'verify.txt' otherwise purge in 15 minutes
                await asyncio.wait_for(check_verify(f"{vCode} {email_addr}", message, temp), timeout=900)
            except asyncio.TimeoutError:
                try:
                    await message.delete(); await temp.delete()
                except errors.NotFound:
                    pass
                edit_file("verify.txt", f"{vCode} {email_addr} {ID} {gender}")
    elif listen_code(message): # Listen for 4-digit code in #verify
        eCode = listen_code(message)
        if eCode:
            with open("verify.txt") as f:
                lines = f.readlines(); flag = True
                if len(lines) != 0:
                    for line in lines:
                        lst = line.strip('\n').split(' ')
                        if lst[0] == eCode.group() and lst[2] == str(message.author.id): # Verify code
                            edit_file("verify.txt", line.strip('\n'))
                            college = re.search(r"(?<=@)\w+", str(lst[1]))
                            guild = bot.get_guild(SERVER_ID); pro = False
                            if college:
                                try:
                                    college_role = COLLEGES[college.group().replace(".edu", '').lower()]
                                    role = get(guild.roles, id=college_role)
                                    await message.author.add_roles(role) # Add Specific College role to user
                                except KeyError:
                                    pro = True
                            if not pro:
                                role = get(guild.roles, name=f"{lst[3]}s Waiting Room")
                                await message.author.add_roles(role) # Add Waiting Room role to user
                            else:
                                role = get(guild.roles, name="Pros Waiting Room")
                                await message.author.add_roles(role) # Add Pro Waiting Room role to user
                            nName = get_name(lst[1]) # New Nick Name
                            await message.delete(); flag = False
                            try:
                                if nName != None: # Re-name user
                                    await message.author.edit(nick=str(nName))
                                else:
                                    nName = lst[1]
                                    await message.author.edit(nick=str(nName))
                            except errors.Forbidden:
                                print("Success!\n", nName)
                            sibling = get_sibling(lst[3]) # Get brother/sister object
                            channel = bot.get_channel(sibling.wait) # Waiting room channel
                            if sibling.wait != PROS.wait:
                                await channel.send(f"@here ***" + message.author.mention + "***" + " *has joined the NJIT MSA Discord!*")
                            else:
                                msg = await channel.send(f"@here ***" + message.author.mention + "***" + " *has joined the NJIT MSA Discord!*")
                                with open("introductions.txt", 'a') as f:
                                    f.write(f"{lst[2]} {msg.id}\n")
                        else:
                            await message.delete(delay=60)
                    if flag:
                        temp = await message.channel.send("**Invalid code! Who a u?!**")
                        await temp.delete(delay=60)
    else: # Delete every other message in #verify in 5 min.
        if message.channel.id == VERIFY_ID:
            if re.search(r"^[a-zA-Z]{2,4}\d{0,4}$", message.content):
                await message.channel.send("**Invalid command! Read instructions above and use /verify please!**", delete_after=25)
            await message.delete(delay=300)
    await bot.process_commands(message)


# Bot Starting Point
if __name__ == "__main__":
    token = BOT
    bot.run(token)
##bot.logout()
##bot.close()
##print("We have logged out of bot bot")
