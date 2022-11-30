import discord


class GuildException(discord.ApplicationCommandError):
    pass


class GuildNotRegistered(GuildException):
    pass


class GuildRegistered(GuildException):
    pass


class RoleException(GuildException):
    pass


class RoleNotExist(RoleException):
    def __init__(self, name=None):
        self.name = name
        super().__init__()

    def __str__(self):
        return f'{super().__str__()} {self.name}'


class ChannelException(GuildException):
    pass


class ChannelNotExist(ChannelException):
    def __init__(self, name=None):
        self.name = name
        super().__init__()

    def __str__(self):
        return f'{super().__str__()} {self.name}'


class AccessException(GuildException):
    def __init__(self, name=None):
        self.name = name
        super().__init__()

    def __str__(self):
        return f'{super().__str__()} {self.name}'


class MissingRole(AccessException):
    pass


class MemberException(GuildException):
    pass


class MemberRegistered(MemberException):
    pass


class MemberNotRegistered(MemberException):
    pass
