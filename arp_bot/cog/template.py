import logging
# declare logger
logger = logging.getLogger(__name__)

from discord.ext import commands
import discord


class Template(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


def setup(bot: commands.Bot):
    bot.add_cog(Template(bot))
