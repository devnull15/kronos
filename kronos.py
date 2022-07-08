# kronos.py

import os
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
import pytz

load_dotenv()
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='/var/log/discord/kronos.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')



@bot.event
async def on_ready():
    logger.info('{} has connected to Discord!'.format(bot.user))

@bot.command()
async def time(ctx):
    tfmt = "%H:%M"
    tz_NY = pytz.timezone('America/New_York') 
    tz_Amsterdam = pytz.timezone('Europe/Amsterdam')
    now_NY = datetime.now(tz_NY)
    now_Amsterdam = datetime.now(tz_Amsterdam)
    now_Server = datetime.now()

    await ctx.send("**New York time:** {}".format(now_NY.strftime(tfmt)))
    await ctx.send("**Amsterdam time:** {}".format(now_Amsterdam.strftime(tfmt)))
    await ctx.send("**Server Time:** {}".format(now_Server.strftime(tfmt)))
    return

@bot.command()
async def egg(ctx):
    await ctx.send("Fuck you Ken")
    return

bot.run(TOKEN)
