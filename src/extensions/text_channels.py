import discord

from const import Strings
from utils.access_modifier import has_permissions, guild_only


class TextChannels:
    @staticmethod
    @guild_only
    @has_permissions("manage_messages")
    async def clean_messages(bot, message: discord.Message):
        contents = message.content.split()
        messages_to_delete = 10

        if len(contents) > 2:
            try:
                messages_to_delete = int(contents[2])
            except (ValueError):
                await message.channel.send(Strings.INTEGER_ONLY)
                return

        deleted = await message.channel.purge(
            limit=messages_to_delete + 1, check=lambda m: m.id != message.id
        )
        await message.channel.send(f"{len(deleted)}개의 메세지를 지웠어요!")

    @staticmethod
    @guild_only
    @has_permissions("manage_channels")
    async def flush_channel(bot, message):
        await message.channel.clone()
        await message.channel.delete()
