#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File            : config_base.py
Author          : GraphLinq Chain
Email           : info@graphlinq.io
Website         : https://graphlinq.io
Repository      : https://github.com/jrbgit/GraphLinq.TelegramBot
Date            : 2023-06-20
Version         : 1.1
Description     : Base Config - Telegram bot for GraphLinq
"""

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

lcw_api_key = LCW_API_KEY
logging.info('[VARIABLE] LiveCoinWatch API Key: {}' .format(lcw_api_key))

# Live Coin Watch
lcw_url = 'https://api.livecoinwatch.com/coins/single'
logging.info('[VARIABLE] Live Coin Watch Single Coin API: {}' .format(lcw_url))

# Locale
#locale.setlocale(locale.LC_ALL, 'en_US')
logging.info('[VARIABLE] Locale is Disabled')

# Fiat to convert using LCW
default_fiat = 'USD'
lcw_fiats_url = 'https://api.livecoinwatch.com/fiats/all'
logging.info('[VARIABLE] Live Coin Watch Fiats: {}' .format(default_fiat))
