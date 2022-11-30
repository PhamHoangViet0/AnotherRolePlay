# __all__ = (
#     'exist',
# )

from discord.ext import commands
import discord
from model import guild as m_guild
from typing import Callable, TypeVar
import app_exception as exc
import asyncio
import inspect
from collections import OrderedDict

T = TypeVar("T")


# def exist() -> Callable[[T], T]:
#     async def predicate(ctx: commands.Context) -> bool:
#         if ctx.guild is None:
#             raise commands.NoPrivateMessage()
#             # raise NoPrivateMessage()
#
#         guild_dc_id = ctx.guild.id
#         if not await m_guild.isExist(guild_dc_id):
#             raise exc.GuildNotRegistered()
#             # raise discord.ApplicationCommandError()
#         # gm_role_id, _ = asyncio.run(mod_guild.getGuild(guild_dc_id))
#         # role = discord.utils.get(ctx.author.roles, id=gm_role_id)
#         # if role is None:
#         #     raise commands.MissingRole(gm_role_id)
#
#         return True
#
#     return commands.check(predicate)
#
#
# def not_exist() -> Callable[[T], T]:
#     async def predicate(ctx: commands.Context) -> bool:
#         if ctx.guild is None:
#             raise commands.NoPrivateMessage()
#             # raise NoPrivateMessage()
#
#         guild_dc_id = ctx.guild.id
#         if await m_guild.isExist(guild_dc_id):
#             raise exc.GuildRegistered()
#             # raise discord.ApplicationCommandError()
#         # gm_role_id, _ = asyncio.run(mod_guild.getGuild(guild_dc_id))
#         # role = discord.utils.get(ctx.author.roles, id=gm_role_id)
#         # if role is None:
#         #     raise commands.MissingRole(gm_role_id)
#
#         return True
#
#     return commands.check(predicate)


def not_exist(guild_model, **kwargs):
    # member_model = kargs.get('member_model')
    if guild_model is not None:
        raise exc.GuildRegistered()


def exist(guild_model, **kwargs):
    # member_model = kargs.get('member_model')
    if guild_model is None:
        raise exc.GuildNotRegistered()



def load(checks=None):
    def decorator(func):
        async def wrapper(self, ctx: commands.Context, *args, **kwargs):
            if ctx.guild is None:
                raise commands.NoPrivateMessage()
                # raise NoPrivateMessage()

            guild_dc_id = ctx.guild.id
            guild_data = await m_guild.get_data(guild_dc_id)
            if guild_data is None:
                raise exc.GuildNotRegistered()

            guild_model = m_guild.Guild(guild_data) if guild_data is not None else None
            kwargs.update({'guild_model': guild_model})
            if checks is not None:
                for check in checks:
                    check(ctx=ctx, **kwargs)

            kwargs.update({'guild_model': guild_model})

            return await func(self, ctx, *args, **kwargs)
        sig = inspect.signature(func)
        parameters = list(sig.parameters.values())
        parameters = [par for par in parameters if par.name != 'guild_model' and par.name != 'kwargs']
        sig = sig.replace(parameters=parameters)
        wrapper.__signature__ = sig
        return wrapper
    return decorator


def have_roles(guild_model: m_guild.Guild, **kwargs):
    if guild_model.gm_role_id is None:
        raise exc.RoleNotExist('gm')
    if guild_model.player_role_id is None:
        raise exc.RoleNotExist('player')
    if guild_model.bot_role_id is None:
        raise exc.RoleNotExist('bot')


def have_channels(guild_model: m_guild.Guild, **kwargs):
    if guild_model.arp_main_category_id is None:
        raise exc.ChannelNotExist('arp_main_category')
    if guild_model.gm_terminal_channel_id is None:
        raise exc.ChannelNotExist('gm_terminal_channel')
    if guild_model.arp_terminal_category_id is None:
        raise exc.ChannelNotExist('arp_terminal_category')
    if guild_model.arp_talk_category_id is None:
        raise exc.ChannelNotExist('arp_talk_category')


def have_all(guild_model: m_guild.Guild, **kwargs):
    have_roles(guild_model=guild_model)
    have_channels(guild_model=guild_model)

