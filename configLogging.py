########################################
######    Initialize   Logging    ######

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
