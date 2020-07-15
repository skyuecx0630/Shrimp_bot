import os
import discord
from subprocess import Popen, check_output

from utils import owners_only
from const import UpdateCommands


class Owners:
    @staticmethod
    @owners_only
    async def get_update(bot, message):
        bot.logger.info("Pulling updates...")

        result = ""

        for command in UpdateCommands:
            result += check_output(command, cwd=bot.BASE_DIR).decode("utf-8")

        for i in range(0, len(result), 2000):
            em = discord.Embed(
                title=f"명령어 실행 결과!", description=result[i : i + 2000], colour=bot.color
            )
            await message.author.send(embed=em)

    @staticmethod
    @owners_only
    async def restart_bot(bot, message):
        file = os.path.join(bot.BASE_DIR, "run.py")

        python = "python3" if os.name == "posix" else "python"
        Popen([python, file])

        await message.add_reaction("\U0001F44C")
        bot.logger.info("Restarting bot...")
        exit()

    @staticmethod
    @owners_only
    async def get_log(bot, message):
        contents = message.content.split()

        log_request = int(contents[2]) if len(contents) > 2 else 10

        log_path = os.path.join(bot.BASE_DIR, "shrimp_bot.log")
        with open(log_path, "r", encoding="utf-8") as f:
            log = f.readlines()[::-1]

            result = "".join(log[:log_request][::-1])

        em = discord.Embed(title="명령어 실행 결과!", description=result, colour=bot.color)

        await message.author.send(embed=em)
