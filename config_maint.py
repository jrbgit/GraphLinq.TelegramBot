#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File            : config_maint.py
Author          : GraphLinq Chain
Email           : info@graphlinq.io
Website         : https://graphlinq.io
Repository      : https://github.com/jrbgit/GraphLinq.TelegramBot
Date            : 2023-06-20
Version         : 1.2
Description     : Maint Config - Telegram bot for GraphLinq
"""

import os
from dotenv import load_dotenv

# Maintenance Mode 0 = Off, 1 = On
maint_mode = os.getenv('MAINT_MODE')

# Admin that can bypass maintenance mode
allowed_admin = os.getenv('ALLOWED_ADMIN')

# Maintenance Mode Messages
maint_mode_msg = 'This bot is in maintenance mode. Check back soon.'
maint_mode_log_msg_on = 'Maintenance Mode is ON!'
maint_mode_log_msg_off = 'Maintenance Mode is OFF!'
