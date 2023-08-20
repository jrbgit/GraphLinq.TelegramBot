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

from config_logging import (logging, log_formats, log_info, log_warning, log_debug,
                            log_error, log_critical)
from config_msgs import (version_msg, sheduler_start_msg,start_msg, help_msg_private, help_msg_public,
    private_msg, websites, socials, staking, shortcuts, cex_listings, dex_listings,status,
    set_address_msg,apply)


def mask_string(s, fraction=0.5):
    # Calculate the number of characters to mask
    mask_length = int(len(s) * fraction)
    # Create a masked string with the appropriate number of asterisks
    masked_part = '*' * mask_length
    # Return the masked string combined with the unmasked part
    return masked_part + s[mask_length:]


# Version
bot_version = '1.1'

# Load .env
load_dotenv()

# Set Variables
LCW_API_KEY = os.getenv('LCW_API_KEY')
TELEGRAM_KEY = os.getenv('TELEGRAM_KEY')

# Telegram Bot Key
telegram = TELEGRAM_KEY
log_info('[SETTINGS] Telegram Bot Token: {}' .format(mask_string(telegram)))

lcw_api_key = LCW_API_KEY
log_info('[SETTINGS] LiveCoinWatch API Key: {}' .format(mask_string(lcw_api_key)))

# Live Coin Watch
lcw_url = 'https://api.livecoinwatch.com/coins/single'
log_info('[SETTINGS] Live Coin Watch Single Coin API: {}' .format(lcw_url))

# Locale
#locale.setlocale(locale.LC_ALL, 'en_US')
log_info('[SETTINGS] Locale is Disabled')

# Fiat to convert using LCW
default_fiat = 'USD'
log_info('[SETTINGS] Custom fiats is Disabled')

lcw_fiats_url = 'https://api.livecoinwatch.com/fiats/all'
log_info('[SETTINGS] Live Coin Watch Fiats: {}' .format(default_fiat))
