import os
from configparser import ConfigParser

config = ConfigParser()

config.read('config.ini')
BOT_TOKEN = os.getenv('BOT_TOKEN', config.get(section='bot', option='token', fallback=None))
if not BOT_TOKEN:
    exit('Please provide bot token environment variable')
