from bot import ShrimpBot
from utils import Timer
from const import Token

timer = Timer()
ShrimpBot().run(Token.token)

print("Run time - %dh : %dm : %ds" % timer.end())
