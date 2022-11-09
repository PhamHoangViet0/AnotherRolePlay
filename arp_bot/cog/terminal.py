import logging
# declare logger
logger = logging.getLogger(__name__)

from discord.ext import commands
import discord
import asyncio
import aioconsole
import aiomysql
import mysql_conn
from decorator import dec_command as dec_com


class Terminal(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @dec_com.terminal_command
    async def shut(self, ctx):
        logger.info("Shutting ...")
        await mysql_conn.close_pool(mysql_conn.pool)
        await self.bot.close()

    @dec_com.terminal_command
    async def check(self, ctx):
        logger.info("Checking")
        conn: aiomysql.Connection
        async with mysql_conn.pool.acquire() as conn:
            cur: aiomysql.Cursor
            async with conn.cursor(aiomysql.DictCursor) as cur:
                query_check = '''SHOW TABLES;'''
                await cur.execute(query_check)
                res = await cur.fetchall()
                print(res)

    @commands.Cog.listener()
    async def on_ready(self):
        await asyncio.sleep(1)
        print("Terminal is listening.")
        while not self.bot.is_closed():
            call = await aioconsole.ainput()
            command = self.bot.get_command('term_' + call)
            if command is not None:
                if command.cog and command.cog.qualified_name == 'Terminal':
                    await command(context=None)
            else:
                print('Unidentified command.')




def setup(bot: commands.Bot):
    bot.add_cog(Terminal(bot))
