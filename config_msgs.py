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
Version         : 1.2
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
    ['Home', 'https://graphlinq.io'],
    ['AI', 'https://ai.graphlinq.io'],
    ['Analytics', 'https://analytics'],
    ['App', 'https://app.graphlinq.io'],
    ['Explorer', 'https://explorer.graphlinq.io'],
    ['Hub', 'https://hub.graphlinq.io'],
    ['Status', 'https://network.graphlinq.io'],
    ['Docs', 'https://docs.graphlinq.io'],
    ['IDE', 'https://ide.graphlinq.io'],
    ['MarketPlace', 'https://marketplace.graphlinq.io']
]

# /socials
socials = [
    ['Twitter', 'https://twitter.com/graphlinq_proto'],
    ['Discord', 'https://discord.com/invite/tCCas5sCWA'],
    ['LinkedIn', 'https://www.linkedin.com/company/graphlinq-protocol'],
    ['YouTube', 'https://www.youtube.com/@graphlinqprotocol4007/videos'],
    ['Reddit', 'https://www.reddit.com/r/graphlinq'],
    ['Medium', 'https://graphlinq.medium.com/']
]

# /staking
staking = [
    ['Website', 'https://app.graphlinq.io/app/staking'],
    ['How-to', 'https://graphlinq.medium.com/glq-staking-migrated-live-on-graphlinq-chain-70a8156d0875']
]

# /documentation
documentation = [
    ['Docs','https://docs.graphlinq.io']
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
    ['KuCoin', 'USDT', 'https://trade.kucoin.com/GLQ-USDT'],
    ['KuCoin', 'BTC', 'https://trade.kucoin.com/GLQ-BTC'],
    ['Gate io', 'USDT', 'https://gate.io/trade/glq_usdt'],
    ['Bilaxy', 'ETH', 'https://bilaxy.com/trade/GLQ_ETH'],
    ['MEXC', 'USDT', 'https://www.mexc.com/exchange/GLQ_USDT'],
    ['CoinEx', 'USDT', 'https://www.coinex.com/exchange/GLQ-USDT'],
    ['CoinTide', 'USDT', 'https://cointide.io/spot/GLQ_USDT']
]

# /buy dex
dex_listings = [
    ['Uniswap v3', 'WETH', 'https://app.uniswap.org/explore/pools/ethereum/0xc3881fbb90daf3066da30016d578ed024027317c'],
    ['QuickSwap v2)', 'ETH', 'https://quickswap.exchange/#/swap?outputCurrency=0x0cfc9a713a5c17bc8a5ff0379467f6558bacd0e0&inputCurrency=0x7ceb23fd6bc0add59e62ac25578270cff1b9f619']
]

# /buy GLQ dex
glq_dex_listings = [
    ['GLQ Hub', 'WETH', 'https://hub.graphlinq.io']
]

# status websites
status = [
    ['Server Status','https://status.graphlinq.io'],
    ['Chain Status','https://network.graphlinq.io']
]

# Developer Application
apply = 'Interested in working for GraphLinq? Contact us today!'
