# import inspect
from discord.ext import commands


def terminal_command(func):
    @commands.command(name=f'term_{func.__name__}')
    async def wrapper(self, context, *args, **kargs):
        if context is not None:
            return None
        return await func(self, context, *args, **kargs)

    # decorator.__name__ = func.__name__
    # decorator.__signature__ = inspect.signature(func)
    return wrapper
