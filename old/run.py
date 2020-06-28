from bot import ShrimpBot
from utils import Timer
from const import Settings
from logger import get_logger

timer = Timer()
logger = get_logger("shrimp_bot")

ShrimpBot(admin=Settings.Admins, logger=logger).run(Settings.token)

logger.info("Run time - %dh : %dm : %ds" % timer.end())
