import logging
# declare logger
# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s]:'
                           '[%(levelname)8s]: '
                           '%(name)s:'
                           '%(funcName)s:'
                           '%(lineno)d: '
                           '%(message)s')
logger = logging.getLogger(__name__)

import discord
from discord.ext import commands

import json
import os
import asyncio
import platform

# fix closing bot
if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from cog import cogInit
import mysql_conn


def start_up():
    config_path = os.path.join('..', 'config')
    with open(os.path.join(config_path, 'bot_config.json'), 'r') as bot_config:
        bot_settings = json.load(bot_config)

    # TO DO: probably should specify intents and move to another file
    bot_intents = discord.Intents.all()

    bot = commands.Bot(command_prefix=bot_settings['prefix'], intents=bot_intents)
    cogInit(bot)

    mysql_conn.loop = bot.loop
    # mysql_conn.loop = asyncio.new_event_loop()
    mysql_conn.pool = mysql_conn.get_pool(mysql_conn.loop)
    # mysql_conn.pool = mysql_conn.get_pool(asyncio.new_event_loop())

    bot.run(bot_settings['token'])


if __name__ == '__main__':
    bot = start_up()
