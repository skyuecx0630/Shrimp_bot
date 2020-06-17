import discord
from discord.ext import commands
import os

from const import Settings
from logger import get_logger
from utils import Timer


def get_prefixes():
    prefix_list = ["새우야 "]
    return prefix_list


class ShrimpBot(commands.Bot):
    def __init__(self, logger=None):
        self.logger = logger
        super().__init__(command_prefix=get_prefixes())

    async def on_ready(self):
        activity = discord.Activity(name="새우야 도움말", type=discord.ActivityType.unknown)
        await self.change_presence(activity=activity)
        self.logger.info("Bot Started!")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    logger = get_logger("shrimp_bot")

    bot = ShrimpBot(logger)

    for extension in os.listdir(os.path.join(BASE_DIR, "cogs")):
        if extension.endswith(".py"):
            bot.load_extension(f"cogs.{extension[:-3]}")

    bot.run(Settings.token)
