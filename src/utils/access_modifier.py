from functools import wraps

from const import Strings, Settings


def owners_only(func):
    @wraps(func)
    async def wrapper(bot, message, *args, **kwargs):
        if message.author.id in Settings.Owners:
            return await func(bot, message, *args, **kwargs)
        else:
            return await message.channel.send(Strings.OWNERS_ONLY)

    return wrapper


def guild_only(func):
    @wraps(func)
    async def wrapper(bot, message, *args, **kwargs):
        if message.guild:
            return await func(bot, message, *args, **kwargs)
        else:
            return await message.channel.send(Strings.GUILD_ONLY)

    return wrapper
