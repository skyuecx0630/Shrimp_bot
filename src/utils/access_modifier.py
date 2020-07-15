import discord
from functools import wraps

from const import Strings, Settings


def owners_only(func):
    @wraps(func)
    async def decorator(bot, message, *args, **kwargs):
        if message.author.id in Settings.Owners:
            return await func(bot, message, *args, **kwargs)
        else:
            return await message.channel.send(Strings.OWNERS_ONLY)

    return decorator


def guild_only(func):
    @wraps(func)
    async def decorator(bot, message, *args, **kwargs):
        if message.guild:
            return await func(bot, message, *args, **kwargs)
        else:
            return await message.channel.send(Strings.GUILD_ONLY)

    return decorator


def has_permissions(*permissions):
    def wrapper(func):
        @wraps(func)
        async def decorator(bot, message, *args, **kwargs):
            user: discord.User = message.author
            user_perms = user.permissions_in(message.channel)

            for perm in permissions:
                if not getattr(user_perms, perm):
                    await message.channel.send(Strings.NO_PERMISSIONS)
            else:
                await func(bot, message, *args, **kwargs)

        return decorator

    return wrapper
