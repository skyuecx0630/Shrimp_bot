import discord
from random import choice

from utils import guild_only
from extensions import Basics
from models import Custom_commands


class CustomCommands:
    @staticmethod
    async def custom(bot, message):
        contents = message.content.split()

        features = {"추가": "add", "삭제": "delete", "목록": "list"}

        try:
            await getattr(CustomCommands, "custom_" + features[contents[2]])(
                message, prefixed=True
            )

        except (IndexError, KeyError):
            await Basics.help(bot, message, command="커맨드")

    @staticmethod
    async def custom_add(bot, message, prefixed=False):
        contents = message.content.split()
        command_index = 3 if prefixed else 1

        try:
            command = contents[command_index]
            output = " ".join(contents[command_index + 1 :])

            if not output:
                raise IndexError

            if bot.command_finder.get_function(command, prefixed=False):
                await message.add_reaction("\U0001F6AB")
                return

        except IndexError:
            await Basics.help(bot, message, command="커맨드")

        else:
            server = str(message.guild.id)
            author = str(message.author.id)
            custom = Custom_commands(server, author, command, output)

            bot.db_manager.insert_row(custom)

            await message.add_reaction("\U0001F44C")

    @staticmethod
    async def custom_show(bot, message):
        contents = message.content.split()

        searched = bot.db_manager.search_row(Custom_commands, "command", contents[0])

        server = str(message.guild.id)
        server_commands = [command for command in searched if command.server == server]

        if server_commands:
            selected = choice(server_commands)

            await message.channel.send(selected.output)

    @staticmethod
    async def custom_delete(bot, message, prefixed=False):
        contents = message.content.split()

        command_index = 3 if prefixed else 1
        try:
            searched = bot.db_manager.search_row(
                Custom_commands, "command", contents[command_index]
            )

        except IndexError:
            await Basics.help(bot, message, command="커맨드")

        else:
            if not searched:
                await message.add_reaction("\U00002753")

            server = str(message.guild.id)
            server_commands = [
                command for command in searched if command.server == server
            ]

            if server_commands:
                for command in server_commands:
                    bot.db_manager.delete_row(command)

                await message.add_reaction("\U0001F44C")

    @staticmethod
    async def custom_list(bot, message, prefixed=False):
        await message.channel.trigger_typing()

        server = str(message.guild.id)
        searched = bot.db_manager.search_row(Custom_commands, "server", server)

        if not searched:
            await message.channel.send("이 서버엔 추가된 커맨드가 없네요!")
            return

        command_dict = {}

        for custom in searched:
            if custom.command in command_dict:
                command_dict[custom.command] += 1
            else:
                command_dict[custom.command] = 1

        title = f"{message.guild.name}의 커맨드 목록"
        description = "\n".join([f"`{command}`" for command in command_dict])

        em = discord.Embed(title=title, description=description, colour=bot.color)

        await message.channel.send(embed=em)
