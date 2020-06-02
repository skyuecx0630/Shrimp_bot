from bot import ShrimpBot
from utils import Timer
from const import Settings

timer = Timer()
ShrimpBot().run(Settings.token)

print("Run time - %dh : %dm : %ds" % timer.end())
