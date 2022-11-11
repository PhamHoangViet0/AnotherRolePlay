__all__ = ['cogInit']

import logging
# declare logger
logger = logging.getLogger(__name__)

from discord.ext import commands


from cog import terminal, guild, member

COG = [terminal, guild, member]


def cogInit(bot: commands.Bot):
    for cog in COG:
        logger.info(f"Activating cog: {cog.__name__}")
        cog.setup(bot)
