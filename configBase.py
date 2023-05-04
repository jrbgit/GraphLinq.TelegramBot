########################################
######      Base   Variables      ######

import logging
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Set Variables
LCW_API_KEY = os.getenv('LCW_API_KEY')
TELEGRAM_KEY = os.getenv('TELEGRAM_KEY')

# Telegram Bot Key
telegram = TELEGRAM_KEY
logging.info('[VARIABLE] Telegram Bot Token: {}' .format(telegram))

lcwApiKey = LCW_API_KEY
logging.info('[VARIABLE] LiveCoinWatch API Key: {}' .format(lcwApiKey))

# Live Coin Watch
lcwUrl = 'https://api.livecoinwatch.com/coins/single'
logging.info('[VARIABLE] Live Coin Watch Single Coin API: {}' .format(lcwUrl))

# Locale
#locale.setlocale(locale.LC_ALL, 'en_US')
logging.info('[VARIABLE] Locale is Disabled')

# Fiat to convert using LCW
defaultFiat = 'USD'
lcwFiatsUrl = 'https://api.livecoinwatch.com/fiats/all'
logging.info('[VARIABLE] Live Coin Watch Fiats: {}' .format(defaultFiat))
