import discord
from discord.ext import commands
import os
import traceback
import aiohttp

from const import Settings
from logger import get_logger
from utils import Timer


def get_prefixes():
    prefix_list = ["새우야 "]
    return prefix_list


class ShrimpBot(commands.Bot):
    def __init__(self, logger=None, **kwargs):
        self.color = 0xFF421A
        self.logger = logger
        super().__init__(get_prefixes(), help_command=None, **kwargs)

    async def on_ready(self):
        activity = discord.CustomActivity(name="새우야 도움말")
        await self.change_presence(activity=activity)
        self.logger.info("Bot Started!")

    async def on_error(self, event_method, *args, **kwargs):
        return super().on_error(event_method, *args, **kwargs)

    async def on_command_error(self, ctx, exception):
        exc_info = "".join(traceback.format_tb(exception.original.__traceback__))
        self.logger.error(exc_info)

        url = Settings.error_webhook

        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(
                url, adapter=discord.AsyncWebhookAdapter(session)
            )

            for i in range(0, len(exc_info), 2000):
                em = discord.Embed(
                    title=f"에러!", description=exc_info[i : i + 2000], colour=self.color,
                )

            await webhook.send(embed=em)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    logger = get_logger("shrimp_bot")

    bot = ShrimpBot(logger, owners_id=Settings.Owners)

    for extension in os.listdir(os.path.join(BASE_DIR, "cogs")):
        if extension.endswith(".py"):
            bot.load_extension(f"cogs.{extension[:-3]}")

    bot.run(Settings.token)
