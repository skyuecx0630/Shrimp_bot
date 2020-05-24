import configparser
from os.path import dirname, exists, join
from bot import ShrimpBot

CONFIG_FILE = join('..', 'config', 'config.ini')

if exists(CONFIG_FILE):
    parser = configparser.ConfigParser()
    parser.read(CONFIG_FILE)
else:
    raise FileNotFoundError('%s doesn\'t exists' % CONFIG_FILE)

token = parser.get("Default", "token")
ShrimpBot().run(token)
print(token)
