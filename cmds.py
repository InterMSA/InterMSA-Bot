import discord

from discord.ext import commands
from discord.utils import get
from discord import Intents
from discord import File
from discord import Embed
from discord import Game
from discord import errors
from discord.utils import escape_markdown
import asyncio, git
from config import *
from tools import *
import random
#import discord
#from discord import embeds
#import discord

#this is a test to see if this change is automated 

intents = Intents.default()
intents.members = True # Subscribe to the privileged members intent.

bot = commands.Bot(command_prefix=COMMAND_PREFIX, help_command=None, intents=intents)

#client 

# Extended InterMSA Bot Commands

# Help command

@bot.command()
async def cmds(ctx):
   '''
   Shows what bot can do
   '''
   if check_admin(ctx) == True: # This is a special list of custom admin commands 
      with open("cmds_for_mods.md") as f: 
        cmds = f.read()

      embed = Embed(color=0xFFD700) #changes the color to golden 
      embed.add_field(name="**About**", value="Hello Mod! these are your commands", inline=False)
      embed.add_field(name="**Commands**", value=cmds, inline=False) 
      embed.add_field(name="Social Media",
                      value="⚡ [Discord Server Link](https://discord.gg/rKFNrvKWqu)\n🕸 [InerMSA Website](https://intermsa.com/)\n💼 [LinkedIn Group]( https://www.linkedin.com/groups/9002140)\n📱 [Instagram](https://www.instagram.com/intermsa/)",
                      inline=False)
      embed.set_author(name = "InterMSA Bot Commands:",icon_url="https://cdn.discordapp.com/attachments/824860377480429588/829180591811461150/InterMSA_Logo.png")
      embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/814602442910072842/838359760037216296/240_F_218846526_SqlIXtk20dEnVcuXvVTGpzUeE3rmLkAe.png")
      await ctx.send(embed=embed)
   else:
      with open("cmds.md") as f:
         cmds = f.read()
      embed = Embed(color=0xadd8e6)
      embed.add_field(name="**About**", value="These commands are accessible to everyone in the server", inline=False)
      embed.add_field(name="**Commands**", value=cmds, inline=False) 
      embed.set_author(name = "InterMSA Bot Commands:",icon_url="https://cdn.discordapp.com/attachments/824860377480429588/829180591811461150/InterMSA_Logo.png")
      embed.add_field(name="Social Media",
                        value="⚡ [Discord Server Link](https://discord.gg/rKFNrvKWqu)\n🕸 [InerMSA Website](https://intermsa.com/)\n💼 [LinkedIn Group]( https://www.linkedin.com/groups/9002140)\n📱 [Instagram](https://www.instagram.com/intermsa/)",
                        inline=False)
      embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/281/white-question-mark_2754.png")
      await ctx.send(embed=embed)

# Manage Bot Server
@bot.command()
async def botserver(ctx, *args): # (WARNING: Do NOT edit this bot command function unless you know what you're doing)
    if len(args) == 0 or int(ctx.author.id) not in DEVS:
        return -1
    cmd = args[0].lower()
    if cmd == "stop":
        print ("test")
        await ctx.send(f"```{MSA} Bot stopped!```"); await asyncio.sleep(1)
        # os.popen("sudo systemctl stop botd"); exit()
        os.popen("tmux kill-session -t MSA"); exit()
    elif cmd == "restart":
        await ctx.send(f"```{MSA} Bot restarted!```"); await asyncio.sleep(1)
        os.popen("cd /home/jake/MSA-Bot")
        os.popen('tmux kill-session -t MSA \; new-session -d -s MSA \; send-keys "python3 main.py" Enter')
    elif cmd == "update":
        await ctx.send(f"```{MSA} Bot CI/CD system triggered!```"); await asyncio.sleep(1)
        os.popen("cd /home/jake/MSA-Bot")
        out = os.popen("sudo ./update_bot.sh"); print("CLI OUTPUT:", out.read())
    elif cmd == "traceback":
      x = os.popen("tmux capture-pane -pt MSA").read()
      await ctx.send(f"```sh\n#Traceback (most recent call last):\n#{x}```")

    else:
        await ctx.send(f"```Error: Command does not exist!```")

@bot.command()
async def ping(ctx):
  await ctx.reply("pong")

@bot.command()
@commands.has_permissions(manage_channels=True, manage_messages=True)
async def poll(ctx: commands.Context, channel: discord.TextChannel, *, message=""):
    """Send message to a specific channel. then adds emojis underneath it"""       
    # print("hey")
    # print ("msg is: ",message)
    custom_emojis = re.findall(r'[^\w\s()\"#/[@;:<>{}`+=~|.!?,-]', message)      
    # print (message)
    x = await ctx.guild.get_channel(channel.id).send(message)
    for index, mystr in enumerate(custom_emojis):
       # x = await message.channel.send(mystr)
       try:
        await x.add_reaction(str(mystr))
       except:
        pass
    await ctx.message.add_reaction ("✅")

    # return await ctx.tick()
    # if message.content.startswith("/poll"):
      # print (message.content)
      # messageContent=message.content.replace ("/poll","")

      # custom_emojis = re.findall(r'[^\w\s()\"#/[@;:<>{}`+=~|.!?,-]', message.content)
      # print (custom_emojis)

# Show role universities 
@bot.command()
async def showunis(ctx, *args):
    with open("uni_library.txt", 'r', encoding="utf-8") as f:
        text = f.read()
        if text == '':
            await ctx.send("`University library reset!`")
        else:
            text = ''
            e = discord.Embed(color=0xFFD700, title='Universities:')
            for uni,role in COLLEGES.items():
                # text += f"{uni} <@&{role}>\n"
              
                e.add_field(name= f'{uni}', value=f" <@&{role}>", inline=True)
            await ctx.send(embed=e) 
            # await ctx.send(text)

# Show role emojis accessible through #role-selection chat
@bot.command()
async def showroles(ctx, *args):
    with open("role_selection.txt", 'r', encoding="utf-8") as f:
        text = f.read()
        if text == '':
            await ctx.send("`Role selections reset!`")
        else:
            parts = ["Brothers", "Sisters", "Professionals"]; c = 0
            text = ''
            for emoji,role in ROLE_EMOJIS.items():
                text += f"{emoji} <@&{role}>\n"
            text += "\n"
            for key,part in SPLIT_ROLES_EMOJIS.items():
                if len(SPLIT_ROLES_EMOJIS[key]) != 0:
                    text += f"__{parts[c]} Selections__\n"
                c += 1
                for emoji,role in part.items():
                    text += f"{emoji} <@&{role}>\n"
            await ctx.send(text)

# Add emoji & role 
@bot.command()
async def adduni(ctx, *args):
    is_admin = check_admin(ctx)
    if not is_admin:
        return -1
    if len(args) == 0:
        await ctx.send(f"`/adduni <university domain name> <@Role>`")
        return 0
    uni = args[0]; role = args[1].replace("<@&", '').strip('>')
    with open("uni_library.txt", 'r+', encoding="utf-8") as f:
        lines = f.readlines()
        entry = f"{uni} {role}\n"
        if entry not in lines:
            f.write(entry)
        else:
            await ctx.send(f"`University already in library!`", delete_after=25)
            return -1
    update_uni_library()
    await ctx.send(f"`University added to library!`", delete_after=25)

# Add emoji & role accessible through #role-selection chat
@bot.command()
async def addrole(ctx, *args):
    is_admin = check_admin(ctx)
    if not is_admin:
        return -1
    if len(args) == 0:
        await ctx.send(f"`/addrole <emoji> <@Role>`\n"
                       "`/addrole <emoji> <@Bro-Role> <@Sis-Role>`")
        return 0
    emoji = args[0]; role = args[1].replace("<@&", '').strip('>')
    if len(args) == 3:
        extra = args[2].replace("<@&", '').strip('>')
    else:
        extra = 0
    with open("role_selection.txt", 'r+', encoding="utf-8") as f:
        lines = f.readlines()
        entry = f"{extra} {emoji} {role}\n"
        if entry not in lines:
            f.write(entry)
        else:
            await ctx.send(f"`Role reaction already exists!`", delete_after=25)
            return -1
    update_role_select()
    await ctx.send(f"`Role reaction added!`", delete_after=25)

# Delete emoji & role based on university domain name
@bot.command()
async def deleteuni(ctx, *args): # Remove role-selection role
    is_admin = check_admin(ctx)
    if not is_admin:
        return -1
    if len(args) != 1:
        await ctx.send(f"`/deleteuni <university domain name>`")
        return 0
    uni = args[0]
    try:
        del(COLLEGES[uni])
    except KeyError:
        pass
    if edit_file("uni_library.txt", uni, exact=False):
        await ctx.send(f"`University removed from library!`", delete_after=25)
    else:
        await ctx.send(f"`University does not exist!`", delete_after=25)

# Delete emoji & role based on emoji
@bot.command()
async def deleterole(ctx, *args): # Remove role-selection role
    is_admin = check_admin(ctx)
    if not is_admin:
        return -1
    if len(args) != 1:
        await ctx.send(f"`/deleterole <emoji>`")
        return 0
    emoji = args[0]
    try:
        del(ROLE_EMOJIS[emoji])
        del(SPLIT_ROLES_EMOJIS[emoji])
    except KeyError:
        pass
    if edit_file("role_selection.txt", emoji, exact=False):
        await ctx.send(f"`Role reaction removed!`", delete_after=25)
    else:
        await ctx.send(f"`Role reaction does not exist!`", delete_after=25)
          #"join
# Add user officially to the Discord server
#print(random.choice(greeting))
quotes = ["Time waits for no one","Time is like a sword if you don't cut it it will cut you",
"Take advantage of five before five, 1) your youth before your old age ...  ", 
"“There are two blessings which many people lose: (They are) health and free time for doing good.” (Bukhari 8/421)", 
"“Yesterday is history, tomorrow is a mystery, but today is a gift. That is why it is called the present.”",
 "The key is in not spending time, but in investing it","plan for the worst hope for the best"
 ,"https://youtu.be/JObb2BYmp2w?t=45","https://www.youtube.com/watch?v=0xe5twFK1SI"]


ball = [
        ("As I see it, yes"),
        ("It is certain"),
        ("It is decidedly so"),
        ("Most likely"),
        ("Outlook good"),
        ("Signs point to yes"),
        ("Without a doubt"),
        ("Yes"),
        ("No"),
        ("Say inshAllah"),
        ("Allah knows"),
        ("say astaghfirullah"),
        ("لا"),
        ("نعم"),
        ("Yes – definitely"),
        ("You may rely on it"),
        ("Reply hazy, try again"),
        ("Ask again later"),
        ("Better not tell you now"),
        ("Cannot predict now"),
        ("Concentrate and ask again"),
        ("Don't count on it"),
        ("My reply is no"),
        ("My sources say no"),
        ("Outlook not so good"),
        ("Very doubtful"),
    ]

@bot.command()
async def quote(ctx):
    print("hey")
    embed = discord.Embed(  
                  color=0xFFD700 )
    embed.add_field(name="**Quote**", value=random.choice(quotes) , inline=False)
      #await ctx.send(random.choice(quotes))
    await ctx.send(embed=embed)
# ------

@bot.command(name="8", aliases=["8ball"])
async def _8(ctx, *, question: str):
    """Ask 8 ball a question.
    Question must end with a question mark.
    """ 
    if question.endswith("?") and question != "?":
        await ctx.send("`" + random.choice(ball) + "`")
    else:
        await ctx.send(("That doesn't look like a question."))

def escape(text: str, *, mass_mentions: bool = False, formatting: bool = False) -> str:
    """Get text with all mass mentions or markdown escaped.
    Parameters
    ----------
    text : str
        The text to be escaped.
    mass_mentions : `bool`, optional
        Set to :code:`True` to escape mass mentions in the text.
    formatting : `bool`, optional
        Set to :code:`True` to escape any markdown formatting in the text.
    Returns
    -------
    str
        The escaped text.
    """

    if mass_mentions:
        text = text.replace("@everyone", "@\u200beveryone")
        text = text.replace("@here", "@\u200bhere")
    if formatting:
        text = discord.utils.escape_markdown(text)
    return text

@bot.command(usage="<first> <second> [others...]")
async def choose(ctx, *choices):
    """Choose between multiple options.
    There must be at least 2 options to pick from.
    Options are separated by spaces.
    To denote options which include whitespace, you should enclose the options in double quotes.
    """
    choices = [escape(c, mass_mentions=True) for c in choices if c]
    
    if len(choices) < 2:
        await ctx.send(("Not enough options to pick from."))
    else:
        # print ("2")
        # print (choices)
        await ctx.send(random.choice(choices))



@bot.command()
async def add(ctx, *args):
   is_admin = check_admin(ctx, add_on="Representative")
   if not is_admin:
      await message.channel.send("**YOU ARE NOT ADMIN WHAT ARE YOU DOING!!!!**")
      return -1
   #print(args[0])   
   if len(args) <= 1: # If user already has full name
      user_id = re.search(r"\d{5,}", args[0])

      if user_id:
         guild = bot.get_guild(SERVER_ID)
         member = guild.get_member(int(user_id.group()))
         sibling, rm_role = get_sibling_role(member)
         if '@' in member.nick:
            await ctx.send("**Please don't leave the user's nickname as email!**", delete_after=25)
            return -1
         role = get(
         bot.get_guild(SERVER_ID).roles, name=f"{sibling}")
         await member.add_roles(role)
         await member.remove_roles(rm_role)
         siblinghood = get_sibling(sibling)

         channel = bot.get_channel(siblinghood.general)
         #await channel.send("<@!" + user_id.group() + "> *has* ***officially*** *joined the InterMSA Discord! Welcome your " + sibling + "!*")
         #ed the interMSA Discord! Please check out <#773420851387301939> to get roles"]

         if str(sibling) == "Brother":
            await channel.send("<@!" + user_id.group() + "> " + random.choice(greeting)+"\ncheck out <#934526938742145054> to get roles")

         if str(sibling) == "Sister":
            await channel.send("<@!" + user_id.group() + "> " + random.choice(greeting)+"\ncheck out <#937494516829679636> to get roles")

      else:
         await ctx.send("**Invalid command! Please make sure you're @ing the user.**", delete_after=25)
         await ctx.delete(delay=300)

   elif(len(args)>1): # If you want to manually nickname user (Pros or non-G-Suite)
      user_id = re.search(r"\d{5,}", args[0])
      if user_id:
         guild = bot.get_guild(SERVER_ID)
         member = guild.get_member(int(user_id.group()))
         sibling, rm_role = get_sibling_role(member)
         role = get(bot.get_guild(SERVER_ID).roles, name=f"{sibling}")
         nName = get_name(member.nick) # get member.name if nick is None

         try:
            if nName != None:
               await member.edit(nick=str(nName))
            else:
               new_name = args[1:]; nName = ''
               for name in new_name:
                    nName += name.capitalize() + ' '
               await member.edit(nick=str(nName).strip(' '))
         except errors.Forbidden:
            print("Success!\n", nName)

         await member.add_roles(role)
         await member.remove_roles(rm_role)
         siblinghood = get_sibling(sibling)
         channel = bot.get_channel(siblinghood.general)

           #"joined the interMSA Discord! Please check out <#773420851387301939> to get roles"]

         if str(sibling) == "Brother":
            await channel.send("<@!" + user_id.group() + "> " + random.choice(greeting)+"Please check out <#934526938742145054> to get roles")

         if str(sibling) == "Sister":
            await channel.send("<@!" + user_id.group() + "> " + random.choice(greeting)+"Please check out <#937494516829679636> to get roles")
            #await channel.send("<@!" + user_id.group() + "> " + random.choice(greeting))

         #await channel.send("<@!" + user_id.group() + "> *has* ***officially*** *joined the InterMSA Discord! Welcome your fellow " + sibling + "!*")
         # read = []
         # if ctx.channel.id == PROS.wait: # Check if in #introductions chat
         #    channel = bot.get_channel(INTROS_ID)
         #    with open("introductions.txt") as f:
         #       for line in f.readlines():
         #          entry = line.strip('\n').split(' ')
         #          if entry[0] == user_id.group():
         #             msg_id = int(entry[1])
         #             msg = await channel.fetch_message(msg_id)
         #             await msg.delete()
         #             read.append(f"{user_id.group()} {msg_id}")
         #    await ctx.message.delete()
         #    for old_msg in read: # Flush msg deletions
         #       edit_file("introductions.txt", old_msg)
      else:
         await ctx.send("**Invalid command! Please make sure you're @ing the user.**", delete_after=25)
         await ctx.message.delete(delay=300)


# Sisters Exclusive Commands
##async def SIS_EXAMPLE_CMD(ctx):
##    if check_gender(ctx.author) == "Sister":
##        print("Sisters command executed!")


# Brothers Exclusive Commands
##async def BRO_EXAMPLE_CMD(ctx):
##    if check_gender(ctx.author) == "Brother":
##        print("Brothers command executed!")


# Handle command errors
@bot.event
async def on_command_error(ctx, error):
    #if isinstance(error, commands.MissingRequiredArgument):
        #if error.param.name == 'when':
    #    await ctx.send("You forgot to give me input! Try `!remind me tomorrow at 2:59pm to send email to prof. Baraa`")

    if isinstance(error, commands.TooManyArguments):
      await ctx.send('too many arguments')
    if isinstance(error, commands.CommandNotFound):
        return
