__all__ = (
    'exist',
)

from discord.ext import commands
import discord
from model import guild
from typing import Callable, TypeVar
import app_exception as exc
import asyncio

T = TypeVar("T")


def exist() -> Callable[[T], T]:
    async def predicate(ctx: commands.Context) -> bool:
        if ctx.guild is None:
            raise commands.NoPrivateMessage()
            # raise NoPrivateMessage()

        guild_dc_id = ctx.guild.id
        if not await guild.isExist(guild_dc_id):
            raise exc.GuildNotRegistered()
            # raise discord.ApplicationCommandError()
        # gm_role_id, _ = asyncio.run(mod_guild.getGuild(guild_dc_id))
        # role = discord.utils.get(ctx.author.roles, id=gm_role_id)
        # if role is None:
        #     raise commands.MissingRole(gm_role_id)

        return True

    return commands.check(predicate)


def not_exist() -> Callable[[T], T]:
    async def predicate(ctx: commands.Context) -> bool:
        if ctx.guild is None:
            raise commands.NoPrivateMessage()
            # raise NoPrivateMessage()

        guild_dc_id = ctx.guild.id
        if await guild.isExist(guild_dc_id):
            raise exc.GuildRegistered()
            # raise discord.ApplicationCommandError()
        # gm_role_id, _ = asyncio.run(mod_guild.getGuild(guild_dc_id))
        # role = discord.utils.get(ctx.author.roles, id=gm_role_id)
        # if role is None:
        #     raise commands.MissingRole(gm_role_id)

        return True

    return commands.check(predicate)