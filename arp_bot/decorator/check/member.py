from discord.ext import commands
import discord
from model import guild as m_guild, member as m_member
from typing import Callable, TypeVar
import app_exception as exc
import asyncio
import inspect


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


def is_gm(ctx: commands.Context, guild_model: m_guild.Guild, **kwargs):
    role = discord.utils.get(ctx.author.roles, id=guild_model.gm_role_id)
    if role is None:
        raise exc.MissingRole('gm')


def is_player(ctx: commands.Context, guild_model: m_guild.Guild, **kwargs):
    role = discord.utils.get(ctx.author.roles, id=guild_model.player_role_id)
    if role is None:
        raise exc.MissingRole('player')


def not_exist(member_model, **kwargs):
    # member_model = kargs.get('member_model')
    if member_model is not None:
        raise exc.MemberRegistered()


def exist(member_model, **kwargs):
    # member_model = kargs.get('member_model')
    if member_model is None:
        raise exc.MemberNotRegistered()


def load(checks=None):
    def decorator(func):
        async def wrapper(self, ctx: commands.Context, guild_model, *args, **kwargs):
            if ctx.guild is None:
                raise commands.NoPrivateMessage()
                # raise NoPrivateMessage()

            author = ctx.author
            member_data = await m_member.get(guild_model.guild_id, author.id)

            member_model = m_member.Member(member_data) if member_data is not None else None
            if checks is not None:
                for check in checks:
                    check(ctx=ctx, guild_model=guild_model, member_model=member_model)

            kwargs.update({'member_model': member_model})

            return await func(self, ctx, guild_model, *args, **kwargs)
        sig = inspect.signature(func)
        parameters = list(sig.parameters.values())
        parameters = [par for par in parameters if par.name != 'member_model' and par.name != 'kwargs']
        sig = sig.replace(parameters=parameters)
        wrapper.__signature__ = sig
        return wrapper
    return decorator
