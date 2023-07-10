#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File            : config_logging.py
Author          : GraphLinq Chain
Email           : info@graphlinq.io
Website         : https://graphlinq.io
Repository      : https://github.com/jrbgit/GraphLinq.TelegramBot
Date            : 2023-06-20
Version         : 1.1
Description     : Logging Config - Telegram bot for GraphLinq
"""

import logging

# Log Settings
logging.basicConfig(
    filename='bot.log',
    encoding='utf-8',
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
# Begin Logging
logging.info('')
logging.info('[STARTING] --==[[ Python Telegram Bot v1.0.6 ]]==--')
logging.info('[VARIABLE] Logging Initialized')
