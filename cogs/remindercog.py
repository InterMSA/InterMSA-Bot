import discord
from discord.ext import tasks, commands
#import json as jason
import datetime
import asyncio
import re,os
import random #for fun, when it sends a reminder, it has a different call
import sys
sys.path.append('..') #goes back one direcrtory to import key
#import asyncpg #post gres database
from config import COMMAND_PREFIX
import pytz
from pytz import timezone #change the timezone to eastern, 
#make sure if you are using putty to change the time on console to America/New_York
#just on console type set-timezone America/New_York
import textwrap #shorting over long text
#import time
#import traceback
from dateparser.search import search_dates #look for time in the sentence
import sqlite3 #storing data on lightwight db
from dateutil import parser #converts strings to to datetime.datetime datatype

#import time

eastern = timezone('US/Eastern')

class ParsedTime:
  def __init__(self, dt, arg):
      self.dt = dt
      self.arg = arg

class TimeConverter(commands.Converter):
  async def convert(self, ctx, argument) -> ParsedTime:
      parsed = search_dates(
          argument, settings={
              'TIMEZONE': 'US/Eastern',
              'PREFER_DATES_FROM': 'future',
              'FUZZY': True
          }
      )
      if parsed is None:
          return None
      elif(parsed [0][0] == "me"):
          return None
      else:
          pass
          #return parsed 

      if not parsed:
          await ctx.send(f"***Invalid Command! see following example***\n (ex: `{COMMAND_PREFIX}remind me in 10 minutes to 'Do HW'\n {COMMAND_PREFIX}remind me next thursday at 3pm to attend MSA event`)")
          embed = discord.Embed(color = discord.Color.red())
          #embed = discord.Embed(title = "",desctiption = "this is desctiption",color=0x461111)
          embed.set_image(url ="https://cdn.discordapp.com/attachments/841054606413791283/871492062665658398/unknown.png")
          #file = discord.File("https://cdn.discordapp.com/attachments/841054606413791283/861802458686816277/unknown.png", filename="...")
          return await ctx.send(embed=embed,delete_after=25)
          raise self.InvalidTimeProvided()
          #raise commands.BadArgument('Invalid time provided. Try again with a different time.') # Time can't be parsed from the argument

      string_date = parsed[0][0]
      date_obj = parsed[0][1]

      now=datetime.datetime.now().astimezone(eastern)
      now = now.replace(tzinfo=None)
      #print ("now: ",now)
      #print ("date_obj: ",date_obj)
      if date_obj <= now: # Check if the argument parsed time is in the past.
          await ctx.send("Time is in the past.")
          raise commands.BadArgument('Time can not be in the past.') # Raise an error.
      
      to_be_passed = f"in {argument}"
      

      if (to_be_passed == "in me"):
        raise commands.BadArgument('Provided time is invalid')

      reason = argument.replace(string_date, "")
      if reason[0:2] == 'me' and reason[0:6] in ('me to ', 'me in ', 'me at '): # Checking if reason startswith me to/in/at
          reason = reason[6:] # Strip it.

      if reason[0:2] == 'me' and reason[0:9] == 'me after ': # Checking if the reason starts with me after
          reason = reason[9:] # Strip it.

      if reason[0:3] == 'me ': # Checking if the reason starts with "me "
          reason = reason[3:] # Strip it.

      if reason[0:2] == 'me': # Checking if the reason starts with me
          reason = reason[2:] # Strip it.

      if reason[0:6] == 'after ': # Checking if the argument starts with "after "
          reason = reason[6:] # Strip it.

      if reason[0:5] == 'after': # Checking if the argument starts with after
          reason = reason[5:] # Strip it.


      return ParsedTime(date_obj.replace(tzinfo=None), reason.strip())

#----------------------------------------------

class MyCog(commands.Cog):
    def __init__(self, bot):
        self.index = 0
        self.bot = bot
        self.yourtask.start()
        
    async def run(self, *args, **kwargs):
      #numnum = os.getenv("BOT_SECRET", yaya_sql())
      self.db = sqlite3.connect('time.sqlite')
      #self.db = await asyncpg.connect(host="localhost",database="reminders",user="postgres",password=numnum)      
      self.yourtask.start()

        #self._task = bot.loop.create_task(self.dispatch_timers())

    def cog_unload(self):
        self.yourtask.cancel()
    print ("- remindercog is up")
 

    @tasks.loop()
    async def yourtask(self):
      # if you don't care about keeping records of old tasks, remove this WHERE and change the UPDATE to DELETE
      #con = connection or self.bot.pool
      #db = sqlite3.connect(mainl)
      db = sqlite3.connect('time.sqlite')
      cursor = db.cursor()

      #next_task = await self.bot.db.fetchrow('SELECT * FROM zam_time WHERE NOT completed ORDER BY expired LIMIT 1')
      cursor.execute('SELECT * FROM zam_time WHERE NOT completed ORDER BY expired')
      next_task = cursor.fetchone()
      # if no remaining tasks, stop the loop
      if next_task is None:
        self.yourtask.stop()
      # sleep until the task should be done
      
      #print (next_task['row_id'])

      now=datetime.datetime.now().astimezone(eastern)
      now = now.replace(tzinfo=None)
      #print(next_task[4])
      #print(now)
      #print("\n")
      #test = next_task[4]

      if next_task is not None:
        guild_id = next_task[1]
        channel_id = next_task[7]
        user_id = next_task[1]
        content =next_task[2]
        url = next_task[8]
        created=next_task[3]
        expired=next_task [4]
        completed=next_task [5]
        
        embed = discord.Embed(  
                     color=0xFFD700 )

        CoolTitle=["Your time has come","You ready?",
        "Reminder","Remember","Remember the 5th of November","Ur timer is up", "ACT NOW", 
        "Stop procrastinating", "Get up there", "Timer","Reminding you"]

        #date = datetime.strptime('2018-11-10 10:55:31', '%Y-%m-%d %H:%M:%S')
        #date_ex = datetime.datetime.strptime(next_task[4], '%Y-%m-%d %H:%M:%S.%f')
        date_ex = parser.parse(next_task[4])
        if date_ex >= now:
          to_sleep = (date_ex- now).total_seconds()
          #print (to_sleep)
          channel = self.bot.get_channel(int(channel_id))
          await asyncio.sleep(to_sleep)
          await channel.send(f"<@{user_id}>")
          embed.add_field(name=random.choice(CoolTitle), value=f"<@{user_id}> {content}\n [Jump to message]({url})" , inline=False)
          await channel.send (embed=embed) 
          #await channel.send(msg)
          my_data=(next_task[6])
          my_query=('''DELETE from zam_time WHERE row_id = ?''')
          db.execute(my_query,(my_data,))
          db.commit()


        else:
          x=next_task[8]
          channel = self.bot.get_channel(int(channel_id))
          
          embed.add_field(name=random.choice(CoolTitle), value=f"<@{user_id}> {content}\n [Jump to message]({url})" , inline=False)
          channel_id = int(channel_id)
          await channel.send(f"<@{user_id}>")
          await channel.send (embed=embed) 
          #channel = self.bot.get_channel(841054606413791283)
          #await channel.send("your task have expired some time ago:")
          my_data=(next_task[6])
          my_query=('''DELETE from zam_time WHERE row_id = ?''')
          db.execute(my_query,(my_data,))
          db.commit()

          #my_data=(next_task[8])
          #my_query=('''UPDATE zam_time SET completed = 1 WHERE row_id = ?''')
          #db.execute(my_query,(my_data,))
          #db.commit()
          #db.execute('')
          #db.commit()
      #await discord.utils.sleep_until(next_task['expired']) #will change this to seconds cacluation 
      #do your task stuff here with `next_task`
      

    # add a `before_loop` and `wait_until_ready` if you need the bot to be logged in
    
#--------------------------------------------------------------------------    
    #@commands.command(pass_context=True) 
    @commands.group(name='reminder', aliases=['remindme', 'remind', "timer"], usage='<when>', invoke_without_command=True)
    async def reminder(self,ctx, *, when: TimeConverter):

      if ((when is None or when.dt is None ) ) : # Make sure 2 arguments were passed - #Error handler to show the correct input
          await ctx.send(f"***Invalid Command! see following example***\n (ex: `{COMMAND_PREFIX}remind me in 10 minutes to 'Do HW'\n {COMMAND_PREFIX}remind me next thursday at 3pm to attend MSA event`)")
          embed = discord.Embed(color = discord.Color.red())
          #embed = discord.Embed(title = "",desctiption = "this is desctiption",color=0x461111)
          embed.set_image(url ="https://cdn.discordapp.com/attachments/841054606413791283/871492062665658398/unknown.png")
          #file = discord.File("https://cdn.discordapp.com/attachments/841054606413791283/861802458686816277/unknown.png", filename="...")
          return await ctx.send(embed=embed,delete_after=25)
          raise self.InvalidTimeProvided()

      #print(f"when is {when.dt}") 
      #print(f"TimeConverter is {TimeConverter.arg}") 
      #print ("here is the time: ")
      now=datetime.datetime.now().astimezone(eastern)

      #sentence = ''
      sentence = ("`"+ '"' +when.arg+'"'+"`")

      await ctx.send(f"**I will remind you  **" + f'<t:{int(when.dt.timestamp())}:R>' +sentence )
      #e.add_field(name= f'<t:{int(expired.timestamp())}:R>', value=f" [{_id}]({url}) {shorten} ...", inline=False)

      user_ID=str(ctx.message.author.id)
      guild_id=str(ctx.message.guild.id)
      channel_id=str(ctx.message.channel.id)
      URL = ctx.message.jump_url

      

      #cursor.execute("SELECT * FROM zam_time WHERE url = ? "
      #  ,URL)
      #ClockIn = cursor.fetchall()

      
      #if not ClockIn:
      now=datetime.datetime.now().astimezone(eastern)
      now = now.replace(tzinfo=None)
      #when.dt = when.dt.replace(tzinfo=None)
      #print(when.dt)
      db = sqlite3.connect('time.sqlite')
      cursor = db.cursor()
      my_data = (user_ID,guild_id,now,when.dt,sentence,URL,channel_id)
      my_query=('''
                  INSERT INTO zam_time(user_id,guild_id, created, expired,content,url,channel_id) VALUES(?,?,?,?,?,?,?)
              ''')

      db.execute(my_query,my_data)
      db.commit()

      #it sleeps
      if self.yourtask.is_running():
        self.yourtask.restart()
      else:
        self.yourtask.start()
          
          #await asyncio.sleep(eta)
          #reminder message after it slept
          #deleting this previous reminder
    @reminder.error
    async def remind_error(self,ctx, error): # Add self as the first param if this is in a cog/class.
        #if isinstance(error, TimeInPast):
        #    await ctx.send("Time is in the past.")
        if isinstance(error, commands.BadArgument):
            await ctx.send(f"Invalid time. Try `{COMMAND_PREFIX}remind me to say salam to my friend in 5 min`")
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'when':
                await ctx.send(f"You forgot to give me input! Try `{COMMAND_PREFIX}remind me an hour min to do HW`")
        if isinstance(error, commands.TooManyArguments):
                await ctx.send(f'Too many arguments.')
              
    @reminder.command(name='list', ignore_extra=False)
    async def reminder_list(self, ctx):
        """Shows the 10 latest currently running reminders."""
        #if not self.ignore_extra:
            #if not view.eof:
                 #raise TooManyArguments('Too many arguments passed to ' + self.qualified_name)
        

        db = sqlite3.connect('time.sqlite')
        cursor = db.cursor()
        query=cursor.execute(f'SELECT * FROM zam_time Where user_id = {str(ctx.author.id)} ORDER BY expired limit 10 ')
        records = cursor.fetchall()

       # ClockIn = await self.bot.db.fetch("SELECT * FROM zam_time WHERE url = $1 ",URL)
        if len(records) == 0:
            return await ctx.send('No currently running reminders.')

        e = discord.Embed(color=0xFFD700, title='Reminders')

        if len(records) == 10:
            e.set_footer(text='Only showing up to 10 reminders.')
        else:
            e.set_footer(text=f'{len(records)} reminder{"s" if len(records) > 1 else ""}')

        #for _id, expired, message,url in records.items():
        #row_id = 6 , ex =4 ,msg=2,8,
        for row in records:
            shorten = row[2]
            shorten = textwrap.shorten(shorten, width=512)

            #print(records['expired'])
            #deadLine=records['expired']
            #expired = expired.strftime("%A at %I:%M%p -- %h/%d/%Y")

            date_ex = parser.parse(row[4])
            e.add_field(name= f'<t:{int(date_ex.timestamp())}:R>', value=f" [{row[6]}]({row[8]}) {shorten} ...", inline=False)


        await ctx.send(embed=e) 

    @reminder.command(name='delete', aliases=['remove', 'cancel'], ignore_extra=False)
    async def reminder_delete(self, ctx, *, id: int):
        """Deletes a reminder by its ID.
        To get a reminder ID, use the reminder list command.
        You must own the reminder to delete it, obviously.
        """
        db = sqlite3.connect('time.sqlite')
        cursor = db.cursor()

        #my_data = ((id,str(ctx.author.id)))
        #my_query = '''DELETE FROM zam_time WHERE row_id =? AND user_id =? '''
        _id = id
        user_ID =str(ctx.author.id)

        cursor.execute(f'SELECT * from zam_time WHERE row_id={_id} AND user_id = {user_ID}')
        next_task = cursor.fetchone()

        my_query=(f'''DELETE from zam_time WHERE row_id={_id} AND user_id = {user_ID} ''')
        #datahey = 
        status = db.execute(my_query)
        db.commit()
        #status = await ctx.db.execute(query, id, str(ctx.author.id))

        if next_task == 'DELETE 0':
            return await ctx.send('Could not delete any reminders with that ID.')
        else:
          if self.yourtask.is_running():
            self.yourtask.restart()
          else:
            self.yourtask.start()

        await ctx.send('Successfully deleted reminder.')

    @yourtask.before_loop
    async def before_yourtask(self):
      #print ('loading tasks...')
      await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(MyCog(bot))
