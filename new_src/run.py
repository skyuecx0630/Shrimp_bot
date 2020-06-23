from handlers import get_logger
from const import Settings

from bot import ShrimpBot


if __name__ == "__main__":
    logger = get_logger("shrimp_bot")

    bot = ShrimpBot(logger)

    bot.run(Settings.token)
