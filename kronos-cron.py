# kronos-cron.py
# <3 dev0
# :)

import os
import logging 
import discord
from dotenv import load_dotenv
from datetime import datetime
import pytz

load_dotenv()
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='/var/log/discord/kronos-cron.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()


@client.event
async def on_ready():
    logger.info('{} has connected to Discord!'.format(client.user))

    if client.is_ws_ratelimited(): #TODO detect rate limit
        logger.error("We're rate limited :( Guess I'll wait...")
        return

    ## TODO abstract all of this so timezone is an arbitrary selection
    ams_channel = None
    ny_channel = None
    tfmt = "%d-%b-%H:%M"
    tz_NY = pytz.timezone('America/New_York') 
    tz_Amsterdam = pytz.timezone('Europe/Amsterdam')
    now_NY = datetime.now(tz_NY)
    now_Amsterdam = datetime.now(tz_Amsterdam)
    now_Server = datetime.now()
    ams_str = "AMS: "
    ny_str = "NY: "
    ams_time = ams_str + now_Amsterdam.strftime(tfmt)
    ny_time = ny_str + now_NY.strftime(tfmt)

    
    for guild in client.guilds:
        for channel in guild.voice_channels:
            if ams_str == channel.name[0:len(ams_str)]:
                ams_channel = channel
            if ny_str == channel.name[0:len(ny_str)]:
                ny_channel = channel
        if ams_channel != None:
            logger.debug("Found Amsterdam Channel in {}: {}; Updating...".format(guild,ams_channel.name))
            await ams_channel.edit(name=ams_time)
        else:
            logger.info("Amsterdam channel not found in {}! Creating...".format(guild))
            await guild.create_voice_channel(name=ams_time, position=0)
        if ny_channel != None:
            logger.debug("Found NY Channel in {}: {}; Updating...".format(guild,ny_channel.name))
            await ny_channel.edit(name=ny_time)
        else:
            logger.info("New York channel not found in {}! Creating...".format(guild))
            await guild.create_voice_channel(name=ny_time, position=0)
    await client.close()
    return

                    

client.run(TOKEN)
