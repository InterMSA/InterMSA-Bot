from discord.ext import commands
from discord.utils import get
from discord import Intents
from discord import File
from discord import Embed
from discord import Game
from discord import errors
import asyncio
from config import *
from tools import *
import discord

#import discord



intents = Intents.default()
intents.members = True # Subscribe to the privileged members intent.
bot = commands.Bot(command_prefix='/', help_command=None, intents=intents)
#client = discord.Client(intents=intents)


# Extended InterMSA Bot Commands


@bot.command()
async def cmds(ctx):
  '''
    Shows what bot can do
  '''
  if check_admin == True: #this is a special mod list with custom commands 
    with open("modCMDS.md") as f: 
        cmds = f.read()

    embed = discord.Embed(  
            color=0xFFD700 ) #changes the color to golden 
    embed.add_field(name="**About**", value="Hello Mod! these are your commands", inline=False)
    embed.add_field(name="**Commands**", value=cmds, inline=False) 
    embed.add_field(name="Social Media",
                        value="➤ [Instagram](https://www.instagram.com/intermsa/) @intermsa\n➤ [website](http://intermsa.com/) http://intermsa.com/\n➤ [Linkin group]( https://www.linkedin.com/groups/9002140) prof. meet\n",
                        inline=False)
    embed.set_author(name = "InterMSA Bot Commands:",icon_url="https://cdn.discordapp.com/attachments/824860377480429588/829180591811461150/InterMSA_Logo.png")

    embed.set_thumbnail(
          url=
          "https://cdn.discordapp.com/attachments/814602442910072842/838359760037216296/240_F_218846526_SqlIXtk20dEnVcuXvVTGpzUeE3rmLkAe.png")
    await ctx.send(embed=embed)

  else:
    with open("cmds.md") as f:
      cmds = f.read()
    embed = discord.Embed(  
            color=0xadd8e6 )
    embed.add_field(name="**About**", value="These commands are accessible to everyone in the server", inline=False)
    embed.add_field(name="**Commands**", value=cmds, inline=False) 
    embed.set_author(name = "InterMSA Bot Commands:",icon_url="https://cdn.discordapp.com/attachments/824860377480429588/829180591811461150/InterMSA_Logo.png")
    embed.add_field(name="Social Media",
                        value="➤ [Instagram](https://www.instagram.com/intermsa/) @intermsa\n➤ [website](http://intermsa.com/) http://intermsa.com/\n➤ [Linkin group]( https://www.linkedin.com/groups/9002140) prof. meet\n",
                        inline=False)
    embed.set_thumbnail(
          url=
          "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/281/white-question-mark_2754.png")
    await ctx.send(embed=embed)


'''
@bot.command()
async def cmds(ctx): # Help command
    if check_admin ==True:
    #if ctx.message.author.check_admin:
      with open("modCMDS.md") as f:
          cmds = f.read()
      await ctx.send("__**InterMSA Bot Commands:**__```CS\n" + cmds + "```")
      #await ctx.send("hello there")
    else:
      with open("cmds.md") as f:
          cmds = f.read()
      await ctx.send("__**InterMSA Bot Commands:**__```CSS\n" + cmds + "```")
'''

# Debug bot
@bot.command()
async def debug(ctx, *args):
  with open("debug.txt") as f:
    status = f.read()
  if args[0] == "start" and status != "start":
    with open("debug.txt", 'w') as f:
      f.write("start")
    status = "start"
    while status == "start":
        await ctx.send("`Discord Bot Live`", delete_after=3600)
        with open("debug.txt") as f:
          status = f.read()
        await asyncio.sleep(3600)
  elif args[0] == "stop" and status != "stop":
    with open("debug.txt", 'w') as f:
      f.write("stop")
  else:
    await ctx.send(f"Debug Status: `{status}`", delete_after=25)

@bot.command()
async def showroles(ctx, *args):
    with open("role_selection.txt", 'r', encoding="utf-8") as f:
        text = f.read()
        await ctx.send(text)

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
            await ctx.send(f"`Role Reaction already exists!`", delete_after=25)
            return -1
    update_role_select()
    await ctx.send(f"`Role Reaction Added!`", delete_after=25)

# Add user officially
@bot.command()
async def add(ctx, *args):
   is_admin = check_admin(ctx, add_on="Representative")
   if not is_admin:
      return -1
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
         await channel.send("<@!" + user_id.group() + "> *has* ***officially*** *joined the InterMSA Discord! Welcome your " + sibling + "!*")
      else:
         await ctx.send("**Invalid command! Please make sure you're @ing the user.**", delete_after=25)
         await ctx.delete(delay=300)
   else: # If you want to manually nickname user (Pros or non-G-Suite)
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
         await channel.send("<@!" + user_id.group() + "> *has* ***officially*** *joined the InterMSA Discord! Welcome your fellow " + sibling + "!*")
         read = []
         if ctx.channel.id == PROS.wait: # Check if in #introductions chat
            channel = bot.get_channel(INTROS_ID)
            with open("introductions.txt") as f:
               for line in f.readlines():
                  entry = line.strip('\n').split(' ')
                  if entry[0] == user_id.group():
                     msg_id = int(entry[1])
                     msg = await channel.fetch_message(msg_id)
                     await msg.delete()
                     read.append(f"{user_id.group()} {msg_id}")
            await ctx.message.delete()
            for old_msg in read: # Flush msg deletions
               edit_file("introductions.txt", old_msg)
      else:
         await ctx.send("**Invalid command! Please make sure you're @ing the user.**", delete_after=25)
         await ctx.message.delete(delay=300)

# Set timer command
@bot.command()
async def timer(ctx, *args):
   is_a_num = re.search(r"^(\d{2,4})$", ''.join(args))
   if is_a_num and len(args) != 2: # Make sure 2 arguments were passed
      await ctx.send("***Invalid Command! Must include hours followed by minutes!***\n (ex: `/time 0 30`)")
   else:
      eta = ((int(args[0]) * 60) * 60) + (int(args[1]) * 60)
      await ctx.send(f"You will be notified in **" + args[0] + "** hour(s) & **" + args[1] + "** minute(s)!")
      await asyncio.sleep(eta)
      await ctx.send(ctx.author.mention + " **ALERT! YOUR TIMER HAS RUN OUT! DO WHAT YOU MUST!**")

# GeoLiberator demo command
@bot.command()
async def GL(ctx, *, arg):
   result = GeoLib.parse_address(arg, "full")
   if result == "OTHER":
      result = GeoLib.parse_address(arg, "address")
   await ctx.send(str(result))


# Sisters Exclusive Commands
##async def SIS_EXAMPLE_CMD(ctx):
##    if check_gender(ctx.author) == "Sister":
##        print("Sisters command executed!")


# Brothers Exclusive Commands
##async def BRO_EXAMPLE_CMD(ctx):
##    if check_gender(ctx.author) == "Brother":
##        print("Brothers command executed!")



@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error
