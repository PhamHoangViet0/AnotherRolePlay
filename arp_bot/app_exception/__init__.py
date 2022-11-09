import discord


class GuildException(discord.ApplicationCommandError):
    pass


class GuildNotRegistered(GuildException):
    pass


class GuildRegistered(GuildException):
    pass