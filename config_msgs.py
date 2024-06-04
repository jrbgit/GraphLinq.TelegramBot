#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File            : config_msgs.py
Author          : GraphLinq Chain
Email           : info@graphlinq.io
Website         : https://graphlinq.io
Repository      : https://github.com/jrbgit/GraphLinq.TelegramBot
Date            : 2023-06-20
Default
Version         : 1.1
Description     : Msgs Config - Telegram bot for GraphLinq
"""

# Version Info
version_msg = '[STARTING] GraphLinq Telegram Bot v'

# Bot Start Msg
sheduler_start_msg = '[SCHEDULE] Starting Scheduler'

# /start
start_msg = [
    ['Welcome to the GraphLinq Telegram Bot.'],
    ['Tip: Type /help to get started.']
]

# /setaddress
set_address_msg = 'First use /setmyaddress to store your address.'

# /help
help_msg = [
    ['Command', 'Description']
]

help_msg_private = [
    ['/setmyaddress', 'Set your address'],
    ['/myaddress', 'View your address'],
    ['/mytotal', 'View your total staked'],
    ['/myrank', 'View your current rank'],
    ['/mytier', 'View your current tier'],
    ['/myrewards', 'View your rewards']
]

help_msg_public = [
    ['/help', 'Display this menu'],
    ['/totalstakers', 'View total stakers'],
    ['/totalstaked', 'View total staked'],
    ['/tiers', 'View total staked/tier'],
    ['/apy', 'View current APY'],
    ###['/top', 'View top 3 stakers'],
    ['/websites', 'List GraphLinq websites'],
    ['/socials', 'List social media links'],
    ['/staking', 'View staking info'],
    ['/documentation', 'View documentation'],
    ['/listings', 'View where to trade GLQ'],
    ['/status', 'Monitor status'],
    ['/apply', 'Developer Application'],
    ['/shortcuts', 'View shortcut commands']
]

# Private Command Response In Public Chat
private_msg = 'This is a private command. Please interact directly with me here @GraphLinqBot'

# /websites
websites = [
    ['Home', 'https://glq.link/home'],
    ['AI', 'https://glq.link/ai'],
    ['Analytics', 'https://glq.link/analytics'],
    ['App', 'https://glq.link/app'],
    ['Explorer', 'https://glq.link/explorer'],
    ['Status', 'https://glq.link/network'],
    ['Docs', 'https://glq.link/docs'],
    ['IDE', 'https://glq.link/ide'],
    ['MarketPlace', 'https://glq.link/marketplace']
]

# /socials
socials = [
    ['Twitter', 'https://glq.link/twitter'],
    ['Discord', 'https://glq.link/discord'],
    ['LinkedIn', 'https://glq.link/linkedin'],
    ['YouTube', 'https://glq.link/youtube'],
    ['Reddit', 'https://glq.link/reddit']
]

# /staking
staking = [
    ['Website', 'https://glq.link/staking'],
    ['How-to', 'https://glq.link/stakingdocs']
]

# /documentation
documentation = [
    ['Docs','https://glq.link/docs']
]

# /shortcuts
shortcuts = [
    ['/setmyaddress', '/setaddress /set'],
    ['/myaddress', '/address'],
    ['/mytotal', '/total'],
    ['/myrank', '/rank'],
    ['/mytier', '/tier'],
    ['/myrewards', '/rewards'],
    ['/totalstakers', '/stakers'],
    ['/totalstaked', '/staked'],
    ['/documentation', '/docs /doc'],
    ['/listings', '/buy /exchanges']
]

# /buy cex
cex_listings = [
    ['KuCoin', 'USDT', 'https://glq.link/kucoinGLQ_USDT'],
    ['KuCoin', 'BTC', 'https://glq.link/kucoinGLQ_BTC'],
    ['Gate io', 'ETH', 'https://glq.link/gateioGLQ_ETH'],
    ['Gate io', 'USDT', 'https://glq.link/gateioGLQ_USDT'],
    ['Bilaxy', 'ETH', 'https://glq.link/bilaxyGLQ_ETH'],
    ['MEXC', 'USDT', 'https://glq.link/mexcGLQ_USDT'],
    ['Biconomy', 'USDT', 'https://glq.link/biconomyGLQ_USDT'],
    ['BitGet', 'USDT', 'https://www.bitget.com/spot/GLQUSDT']
]

# /buy dex
dex_listings = [
    ['Uniswap', 'WETH', 'https://glq.link/uniswapv3'],
]

# status websites
status = [
    ['Server Status','https://glq.link/status'],
    ['Chain Status','https://glq.link/network']
]

# Developer Application
apply = 'Interested in working for GraphLinq? Apply here: https://glq.link/apply'
