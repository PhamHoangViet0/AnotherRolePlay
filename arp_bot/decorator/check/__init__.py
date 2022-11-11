from discord.ext import commands
import decorator.check.guild as guild
import decorator.check.member as member
import inspect


def check_model(checks=None):
    def decorator(func):
        async def wrapper(self, ctx: commands.Context, *args, **kwargs):
            if ctx.guild is None:
                raise commands.NoPrivateMessage()
                # raise NoPrivateMessage()

            if checks is not None:
                for check in checks:
                    check(ctx=ctx, **kwargs)

            return await func(self, ctx, *args, **kwargs)
        
        sig = inspect.signature(func)
        parameters = list(sig.parameters.values())
        parameters = [par for par in parameters if par.name != 'kwargs']
        sig = sig.replace(parameters=parameters)
        wrapper.__signature__ = sig
        return wrapper
    return decorator
