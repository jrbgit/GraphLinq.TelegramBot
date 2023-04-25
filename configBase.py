########################################
######      Base   Variables      ######

import logging

# Telegram Bot Key
telegram = ''
logging.info('[VARIABLE] Telegram Bot Token: {}' .format(telegram))

# Live Coin Watch
lcwUrl = 'https://api.livecoinwatch.com/coins/single'
logging.info('[VARIABLE] Live Coin Watch API: {}' .format(lcwUrl))

# Locale
#locale.setlocale(locale.LC_ALL, 'en_US')
logging.info('[VARIABLE] Locale is Disabled')

# Fiat to convert using LCW
defaultFiat = 'USD'
logging.info('[VARIABLE] Default Fiat: {}' .format(defaultFiat))
