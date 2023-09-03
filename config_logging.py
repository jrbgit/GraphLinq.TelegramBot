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

loggers = {}

telegram_bot_logger = logging.getLogger('telegram')
file_handler = logging.FileHandler('logs/telegram_bot_debug.log')
formatter = logging.Formatter('[%(levelname)s] [%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(formatter)
telegram_bot_logger.addHandler(file_handler)


log_formats = {
    logging.DEBUG: {
        'filename': 'logs/debug.log',
        'encoding': 'utf-8',
        'format': '[DEBUG] [%(asctime)s] %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S'
    },
    logging.INFO: {
        'filename': 'logs/info.log',
        'encoding': 'utf-8',
        'format': '[INFO] [%(asctime)s] %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S'
    },
    logging.WARNING: {
        'filename': 'logs/warning.log',
        'encoding': 'utf-8',
        'format': '[WARNING] [%(asctime)s] %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S'
    },
    logging.ERROR: {
        'filename': 'logs/error.log',
        'encoding': 'utf-8',
        'format': '[ERROR] [%(asctime)s] %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S'
    },
    logging.CRITICAL: {
        'filename': 'logs/critical.log',
        'encoding': 'utf-8',
        'format': '[CRITICAL] [%(asctime)s] %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S'
    }
}

for level, settings in log_formats.items():
    logger = logging.getLogger(str(level))
    logger.setLevel(level)

    file_handler = logging.FileHandler(filename=settings['filename'], encoding=settings['encoding'])
    formatter = logging.Formatter(settings['format'], datefmt=settings['datefmt'])
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    loggers[level] = logger

def log_debug(message):
    loggers[logging.DEBUG].debug(message)

def log_info(message):
    loggers[logging.INFO].info(message)

def log_warning(message):
    loggers[logging.WARNING].warning(message)

def log_error(message):
    loggers[logging.ERROR].error(message)

def log_critical(message):
    loggers[logging.CRITICAL].critical(message)

