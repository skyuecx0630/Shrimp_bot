import configparser
from os.path import dirname, exists, join

from bot import ShrimpBot
from utils import Timer

CONFIG_FILE = join('..', 'config', 'config.ini')

if exists(CONFIG_FILE):
    parser = configparser.ConfigParser()
    parser.read(CONFIG_FILE)
else:
    raise FileNotFoundError('%s doesn\'t exists' % CONFIG_FILE)

token = parser.get("Default", "token")

timer = Timer()
ShrimpBot().run(token)

print("Run time - %dh : %dm : %ds" % timer.end())
