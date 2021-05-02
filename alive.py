# -*- coding: utf-8 -*-
'''
بسم الله
Author: David J. Morfe
Application Name: MSA-Bot
Functionality Purpose: An agile Discord Bot to fit any MSA's needs
'''


import re, os, sys, time
from cmds import *
from config import *
from tools import *


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
   await bot.change_presence(activity = Game(name = "/cmds (For all cmds)"))
   print("We have logged in as {0.user} in {1}".format(bot, ENV))
   try:
      chan = int(input("Enter Channel ID: "))
      channel = bot.get_channel(chan)
   except ValueError:
      print("Wrong type!")
      chan = 778053859536273459
      channel = bot.get_channel(chan)
   while True:
      reply = str(input("reply here: "))
      await channel.send(reply)

# Standard MSA Bot Commands
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return -1;

# Bot Starting Point
if __name__ == "__main__":
    token = BOT
    bot.run(token)
##bot.logout()
##bot.close()
##print("We have logged out of bot")
