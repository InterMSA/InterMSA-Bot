from discord.ext import commands
from discord.utils import get
from discord import Intents
from discord import Embed
from discord import Game
from discord import errors
import asyncio
from config import *
from tools import *


intents = Intents.default()
intents.members = True # Subscribe to the privileged members intent.
bot = commands.Bot(command_prefix='/', help_command=None, intents=intents)
#client = discord.Client(intents=intents)


# Extended InterMSA Bot Commands
@bot.command()
async def help(ctx): # Help command
    with open("cmds.md") as f:
        cmds = f.read()
    await ctx.send("__**CaliBot Commands:**__```CSS\n" + cmds + "```")

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
         nName = get_name(member.nick)
         try:
            if nName != None:
               await member.edit(nick=str(nName))
            else:
               nName = ' '.join(args[1:])
               await member.edit(nick=str(nName))
         except errors.Forbidden:
            print("Success!\n", nName)
         await member.add_roles(role)
         await member.remove_roles(rm_role)
         siblinghood = get_sibling(sibling)
         channel = bot.get_channel(siblinghood.general)
         await channel.send("<@!" + user_id.group() + "> *has* ***officially*** *joined the InterMSA Discord! Welcome your fellow " + sibling + "!*")
         read = []
         if ctx.channel.id == PROS.wait: # Check if in #introductions chat
            channel = bot.get_channel(792530124560924677)
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
   get = re.sub(r"^/GL ", '', str(arg))
   result = GeoLib.parse_address(get, "full")
   if result == "OTHER":
      result = GeoLib.parse_address(get, "address")
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
