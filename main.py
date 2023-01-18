'''
* you run this file so the project becomes alive
1) Make sure you have a token under folder named secrets view file key.py
2) Make sure to configure config.py to be same settings (channel ID) as your server`
3) review bottom of config in order to set up your MSA server
'''

# -*- coding: utf-8 -*-
'''
Author: David J. Morfe && Baraa Nassar
Application Name: InterMSA-Bot
Functionality Purpose: An agile Discord Bot to fit InterMSA's needs
'''

RELEASE = "v1.0.0 - 1/16/2023 - d.py2.1"


import re, os, sys, time, json, datetime
from discord.utils import get
import discord
from config import *
from tools import *
from discord import ui
import random
from discord import Embed
from discord.ext import commands
from discord import app_commands
# from discord.utils import get


RUN_TIME = datetime.datetime.now()
LAST_MODIFIED = RUN_TIME.strftime("%m/%d/%Y %I:%M %p")
RELEASE += f" ({ENV})"

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
# Standard InterMSA Bot Commands, message.content


class Confirm(discord.ui.View): #a verification form once the user clicks Confirm
    def __init__(self):
        super().__init__(timeout=None)
        # super().__init__()
        self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label='Verify', style=discord.ButtonStyle.green, custom_id='persistent_view:green')    
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Questionnaire())
        # await interaction.response.send_message('Confirming', ephemeral=True)
        self.value = True
class Dropdown(discord.ui.Select):
    def __init__(self):

        # Set the options that will be presented inside the dropdown
        options = [
            discord.SelectOption(label="InterMSA",description='What is interMSA?', emoji='🤔'),
            discord.SelectOption(label="Famous Events",description='What are the Most Famous events?', emoji='🌟'),
            discord.SelectOption(label="Resume Review",description='How do I sign up for resume review?', emoji='📰'),
            discord.SelectOption(label="Mock interview",description='How to enroll for mock interview?', emoji='💼'),
            discord.SelectOption(label="Member - volunteer",description='How do I become a member or a volunteer?', emoji='👥'),
            discord.SelectOption(label='Is interMSA an MSA?', emoji='🚪'),
            discord.SelectOption(label='Social Media?', emoji='📱'),
        ]

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Choose your Question...', min_values=1, max_values=1, options=options, custom_id='persistent_view:dropdown')
    
    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
        # print (self.values[0])
        if str(self.values[0]) == "InterMSA":
            await interaction.response.send_message('[I.](https://media.discordapp.net/attachments/751241894805110817/1015479899269627924/unknown.png?width=421&height=632) InterMSA is an independent org that aims to build a network that connects between muslim professionals and undergrads. We also aim to develop young leaders so they can spark on their fields.\n `you may read more here:` [interMSA](https://intermsa.com/ \"Hovertext\") ',ephemeral=True)
        
        if str(self.values[0]) == "Famous Events":
            # os.chdir("./FAQ")
            FAQ = os.getenv("famous_events", famous())
            await interaction.response.send_message(FAQ, ephemeral=True)

        if str(self.values[0]) == "Resume Review":
            await interaction.response.send_message("`Visit this link` \n or \n`Open a ticket on` #ticket\nhttps://intermsa.com/prep", ephemeral=True)
        if str(self.values[0]) == "Mock interview":
            await interaction.response.send_message("`Visit this link` \n or \n`Open a ticket on` #ticket\nhttps://intermsa.com/prep", ephemeral=True)
        
        if str(self.values[0]) == "Member - volunteer":
            FAQ = os.getenv("volunteer", volunteer())
            await interaction.response.send_message(FAQ, ephemeral=True)

        

        if str(self.values[0]) == "Is interMSA an MSA?":
            await interaction.response.send_message("**Nope**\nWe’re an independent org that develops young adults including YMs, MSAs, and other young professionals\nVisit question #1 for more info", ephemeral=True)
        if str(self.values[0]) == "Social Media?":
            await interaction.response.send_message("<https://linktr.ee/intermsa>", ephemeral=True)

class DropdownView(discord.ui.View): #drop down list for FAQ
    def __init__(self):
        super().__init__(timeout=None)
        # Adds the dropdown to our view object.
        self.add_item(Dropdown())

class Bot(commands.Bot): #bot status and running here
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(command_prefix=commands.when_mentioned_or('>'), intents=intents)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        # bot = commands.Bot(command_prefix="!", activity=..., status=...)

        # await bot.change_presence(activity = discord.Game(name = "Yo Salam"))
        print('------')
        guild = bot.get_guild(777022217284354079)
        member = guild.get_member((761123575021174784))

        #Debugging purpuses:
        # *********************************************************************
        # print(get_sibling_role(member))
        # print(member)

        # print (member.roles())
        # c_role = guild.get_role(1015024788474961920)
        # print (c_role)
        # new_role = guild.create_role(name="test")

        # channel = bot.get_channel(1012549840447746048) #verify channel
        # view = Confirm()
        # print(BROTHERS.wait)

        # guild = 751241894805110814
        # c_role = get(guild.roles, name="NJIT")
        # await interaction.user.add_roles(c_role)
        # await channel.send ('Do you want to continue?', view=view)
        # *********************************************************************


    async def setup_hook(self) -> None: #hook so the dropdown and the button work even when the bot restarts
        self.add_view(Confirm())
        self.add_view(DropdownView())

bot = Bot()


@bot.event
async def on_message(message,*args): #On msg.content response 
    if message.author == bot.user:
        return -1;
    # Exclusive Experimental Commands
    userMessage = message.content.lower() 

    if (userMessage.startswith("flip a coin")) or (userMessage.startswith("flip coin")):
        faceCoin = ["heads","tails"]
        await message.reply(random.choice(faceCoin))

    dice=["dice",'die','di','dic']
    if userMessage.startswith(f"roll a di"):
        await message.reply("🎲"+str(random.randint(1,6)))

    if (message.content.startswith('>fetch') or message.content.startswith('>add')): # Add user officially  in case the >add doesn't work, this is a backup
       #you cannot write the names with this command
       # /add or >add @username

       is_admin = check_admin(message, add_on="Admin")
       if not is_admin:
          return -1
       #if len(args) <= 1: # If user already has full name

       if is_admin:
          user_id = re.search(r"\d{5,}", message.content)
          #user_id = re.search(r"\d{5,}", args[0])
          #print (args[0])
          if user_id:
             guild = bot.get_guild(SERVER_ID)
             member = guild.get_member(int(user_id.group()))

             sibling = get_sibling_role(member)
             rm_role = get_sibling_role(member)
             # print ("guild is", guild)
             #print("type guild is",type(guild))
             # print ("groupID", (int (user_id.group())))

             role = get(bot.get_guild(SERVER_ID).roles, name=f"{sibling}")
             rm_role =  get(bot.get_guild(SERVER_ID).roles, name=f"{sibling}s Waiting Room")
             not_verify_role = discord.utils.get(guild.roles, name = 'not-verified')

             await member.add_roles(role)
             # await member.remove_roles(rm_role,not_verify_role)
             await member.remove_roles(rm_role)
             await member.remove_roles(not_verify_role)

             siblinghood = get_sibling(sibling)
             channel = bot.get_channel(siblinghood.general)
             #channel = bot.get_channel(9248729487408)

               #"joined the interMSA Discord! Please check out <#773420851387301939> to get roles"]

             if str(sibling) == "Brother":
                await channel.send("<@!" + user_id.group() + "> " + random.choice(greeting)+"Please check out <#934526938742145054> to get roles")

             if str(sibling) == "Sister":
                await channel.send("<@!" + user_id.group() + "> " + random.choice(greeting)+"Please check out <#937494516829679636> to get roles")
                #await channel.send("<@!" + user_id.group() + "> " + random.choice(greeting))

          else:
             await message.channel.send("**Invalid command! Please make sure you're @ing the user.**", delete_after=25)
             await message.delete(delay=300)

          #else:
          #   await ctx.send("**Invalid command! Please make sure you're @ing the user.**", delete_after=25)
             #await ctx.delete(delay=300)

    # Exclusive Experimental Commands
    if message.content == "carmoosa":
        if "carmoosa#5895" == str(message.author):
            await message.channel.send("nu nu")
    if message.content == 'nu u':
        if "Cali#6919" == str(message.author):
            await message.channel.send("nu u!")
    
    if message.content.lower().startswith('>version'):
        # print(f"`{RELEASE} | {LAST_MODIFIED}`")
        is_admin = check_admin(message) #anyone who's an admin can run /version
        if is_admin:
            await message.channel.send(f"`{RELEASE} | {LAST_MODIFIED}`")
            
    if re.search("(nu nu|Nunu|nunu)", message.content): # Taha
        if message.author.id == 496079190475538461:
            await message.channel.send("nu nu?")
    if message.content.startswith("/suggest"):
      #if message.channel.id == 785554461367468073:#suggestion channel
        thumbsUp = '\N{THUMBS UP SIGN}' #thumbs up emoji
        thumbsDown = "\U0001F44E" #thumbs down emoji

        await message.add_reaction(thumbsUp)
        await message.add_reaction(thumbsDown)


    if "/taha" in message.content.lower(): # Taha
        if message.author.id == 496079190475538461:
            await message.channel.send("Yes we can")

    if "ws" == message.content:
        await message.channel.send("Walaikumu Salam")
    
    if message.content.lower().startswith("/baraa"): # Baraa
        if message.author.id == 670325339263860758:
          await message.channel.send("very well inshAllah")

    # if re.search("(tired|sleep|night)", message.content.lower()):
    #     if message.author.id == 508654889002467329:
    #         await message.channel.send("***Never wake the sleeping Hafeth!***")
    if "choco" in message.content.lower():
        if message.author.id == 732373611775524926:
            lst = ["https://tenor.com/view/chocolate-spongebob-fish-rage-love-chocolate-gif-4938413",
                   "https://tenor.com/view/spongebob-chocolate-gif-9718522",
                   "https://tenor.com/view/kermit-the-frog-chocolate-gif-18833858"]
            r_i = randint(0,2)
            await message.channel.send(str(lst[r_i]), delete_after=30)

    # Professional Introductions Chat
    if message.channel.id == PROS.wait:
        if not message.content.startswith(">add "):
            with open("introductions.txt", 'a') as f:
                user_id = str(message.author.id)
                msg_id = str(message.id)
                f.write(f"{user_id} {msg_id}\n")
            await message.delete(delay=600)

    # Shared Announcment System
    if listen_announce(message): # Send to alternate announcement channel
        announce_channel = listen_announce(message)
        channel = bot.get_channel(announce_channel)
        try:
          ext = re.search(r".(png|jpg|jpeg|mp4)$", message.attachments[0].url)
        except IndexError:
          ext = None
        if len(message.attachments) == 1 and ext:
            file_name = "imgs/reattach" + str(ext.group())
            with open(file_name, "wb") as f:
                await message.attachments[0].save(f)
            img = File(file_name)
            await channel.send(message.content, file=img)
            os.remove(file_name)
        else:
            await channel.send(message.content)
    
    await bot.process_commands(message)



@bot.command() #the trigger that sends the FAQ
async def colour(ctx):
    """Sends a message with our dropdown containing colours"""
    # Create the view containing our dropdown
    view = DropdownView()

    # Sending a message containing our view
    await ctx.send('Frequently Asked Questions', view=view)

@bot.command()
async def ask(ctx: commands.Context): #the trigger that sends the verify form
    """Asks the user a question to confirm something."""
    # We create the view and assign it to a variable so we can wait for it later.
    view = Confirm()
    await ctx.send('Click below to continue', view=view)
    # Wait for the View to stop listening for input...
    await view.wait()
    if view.value is None:
        print('Timed out...')
    elif view.value:
        print('Confirmed...')
    else:
        print('Cancelled...')




@bot.command()
async def cmds(ctx):
   '''
   Shows what bot can do
   '''
   if check_admin(ctx) == True: # This is a special list of custom admin commands 
      # FAQ = os.getenv("famous_events", famous())
      cmds = os.getenv("cmd_commands", mod_commands())
      # cmds = os.getenv("volunteer", commands())

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
      cmds = os.getenv("commands", com())

      embed = Embed(color=0xadd8e6)
      embed.add_field(name="**About**", value="These commands are accessible to everyone in the server", inline=False)
      embed.add_field(name="**Commands**", value=cmds, inline=False) 
      embed.set_author(name = "InterMSA Bot Commands:",icon_url="https://cdn.discordapp.com/attachments/824860377480429588/829180591811461150/InterMSA_Logo.png")
      embed.add_field(name="Social Media",
                        value="⚡ [Discord Server Link](https://discord.gg/rKFNrvKWqu)\n🕸 [InerMSA Website](https://intermsa.com/)\n💼 [LinkedIn Group]( https://www.linkedin.com/groups/9002140)\n📱 [Instagram](https://www.instagram.com/intermsa/)",
                        inline=False)
      embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/281/white-question-mark_2754.png")
      await ctx.send(embed=embed)


class Questionnaire(ui.Modal, title='Questionnaire Response'): #form labels
    name = ui.TextInput(label='Name')
    # answer = ui.TextInput(label='Answer', style=discord.TextStyle.paragraph)
    college = ui.TextInput(label='College Name', style=discord.TextStyle.short)
    email = ui.TextInput(label='Email', placeholder= "person@montclair.edu", style=discord.TextStyle.short)
    #Use the email to send a msg to the person who verified stating that someone has joined the server with their mail
    #If it wasn't them then they should let us know about it. 
    #also put the name that they put
    isStudent = ui.TextInput(label='are you a pro or student', placeholder="pro or student", style=discord.TextStyle.short)
    gender = ui.TextInput(label='gender', placeholder="brother or sister?", style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
            # self.name
            # self.college
            # self.email
            # self.isStudent
            # self.gender
        # await interaction.response.send_message(f'Thanks for your response, {self.name}!', ephemeral=True)
        await interaction.user.edit(nick=str(self.name))
        email_addr = str(self.email)
        gender =str(self.gender).capitalize() #!!!
        Pro_Student=str(self.isStudent)

        if get_sibling(gender) == None :

        # if not re.search(r"(bro(ther)?s?|sis(tas?|ters?)|work(force)?)", gender):
            return await interaction.response.send_message('Please enter Correct Gender `brother` or `sister`', ephemeral=True)
       
        elif not re.search(r"^.+@.+\.", email_addr):
            return await interaction.response.send_message('Please enter Correct email address', ephemeral=True)
        
        elif ((Pro_Student.lower()!="pro") and not (Pro_Student.startswith("st"))):
            return await interaction.response.send_message('Please enter Correct values `Pro` or `student`', ephemeral=True)

        else:
            # await interaction.response.send_message(f'Thanks for your response,\nname: {self.name} \ncollege: {self.college}\nemail: {self.email}\npro? {self.isStudent}\ngender: {self.gender}!', ephemeral=True)
            await interaction.response.send_message(f'Thanks for your response, please wait until an admin adds you :) ',ephemeral=True)

        # print (email_addr)

        college = re.search(r"\w+(?=\.edu)", str (email_addr))
        guild = bot.get_guild(SERVER_ID); pro = False; c_role = "N/A"
       

        if (Pro_Student.lower()=="student") or (Pro_Student.startswith("st")):
            try:
                college = college.group().lower()
                college_role = COLLEGES[college]
                c_role = guild.get_role(college_role)
                # c_role = get(guild.roles, id=1016085193821536387)
                # print (f"college_role: {college_role}")
                # print (f"c_role: {c_role}")
                # c_role = get(guild.roles, name="NJIT")
                await interaction.user.add_roles(c_role) # Add Specific College role to user
            except: # If college domain not registered under InterMSA
                pass
        else:
            pro = True; gender = "Pro"

        if not pro or ".edu" not in email_addr:
            # print(gender)

            role = get(guild.roles, name=f"{gender}s Waiting Room")
            await interaction.user.add_roles(role) # Add Waiting Room role to user
        else:
            role = get(guild.roles, name="Pros Waiting Room")
            await interaction.user.add_roles(role) # Add Pro Waiting Room role to user
        # nName = get_name(str(email_addr)) # New Nick Name
        flag = False

        await interaction.user.edit(nick=str(self.name))

        # sibling = ""
        # if not pro:
        #     if self.gender == "brother":
        #         sibling = brother
        #     elif self.gender == "sister":
        #         sibling = "sister"

        gender = str(self.gender).capitalize()
        sibling = get_sibling(gender) # Get brother/sister/pro object
        # print (f"sibling is: {sibling}")
        if sibling.wait != PROS.wait: # bro/sis wait channel
            # channel = bot.get_channel(814602442910072842) # Waiting room channel for testing
            # print("hey")
            channel = bot.get_channel(sibling.wait) # Waiting room channel
            if pro == True:
                channel = bot.get_channel(PROS.wait)
                await channel.send(f"@here " + interaction.user.mention + " *has joined the InterMSA Discord!*")
                await channel.send("`Note: user will join pro chat by default because college is not registered under InterMSA!`")
                await channel.send(f'> name: {self.name} from **{self.college}**\n> email: **{self.email}**\n> **{self.isStudent}** gender: **{self.gender}**!')
            
            else:
                #channel = bot.get_channel(814602442910072842) discord-bot channel for debuging
               #if str(channel) == "bro-wait" or str(channel)=="discord-bot" :
                if str(channel) == "bro-wait": 
                    #await channel.send(f"*** You came from {c_role.mention} " + message.author.mention + "***" + " *please wait until <@&780660920363515914> adds you*")
                    channel

                    await channel.send(f"Salam "+interaction.user.mention+f"! please wait until <@&780660920363515914> to add you ")
                    await channel.send(f'> name: {self.name} from **{self.college}**\n> email: **{self.email}**\n> **{self.isStudent}** gender: **{self.gender}**!')
        
                elif str(channel) == "sis-wait":
                    await channel.send(f"Salam "+interaction.user.mention+f"! please wait until <@&792258252062064670> to add you")
                    await channel.send(f'> name: {self.name} from **{self.college}**\n> email: **{self.email}**\n> **{self.isStudent}** gender: **{self.gender}**!')
                # else:
                    # await channel.send("yo")
        # else: # pro wait channel
        #     channel = bot.get_channel(sibling.wait) # Waiting room channel
        #     msg = await channel.send(f"@here " + message.author.mention + " *has joined the InterMSA Discord!*", delete_after=60)
        else: # pro wait channel
            channel = bot.get_channel(sibling.wait) # Waiting room channel
            msg = await channel.send(f"@here " + message.author.mention + " *has joined the InterMSA Discord!*")
            await channel.send(f'> name: {self.name} from **{self.college}**\n> email: **{self.email}**\n> **{self.isStudent}** gender: **{self.gender}**!')

#some other fun commands:

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




# Bot Starting Point


if __name__ == "__main__":
    token = BOT
    bot.run(token)

##bot.logout()
##bot.close()
##print("We have logged out of bot bot")
