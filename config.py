import logging
import os
from dotenv import load_dotenv
from web3 import Web3
import json


########################################
######      Base   Variables      ######

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



########################################
######    Initialize   Logging    ######

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



#########################################
###### Maintenance  Mode  Settings ######

# Maintenance Mode 0 = Off, 1 = On
maintMode = 1

# Admin that can bypass maintenance mode
allowedAdmin = 1392716682

# Maintenance Mode Messages
maintModeMsg = 'This bot is in maintenance mode. Check back soon.'
maintModeLogMsgOn = 'Maintenance Mode is ON!'
maintModeLogMsgOff = 'Maintenance Mode is OFF!'



########################################
######      Bot  Reply  Text      ######

# /setaddress
setAddressMsg = 'You must first use the /setaddress command to store your address. example: /set 0xYourAddressGoesHere'

# /help
helpMsg = 'COMMANDS\n\n/help [this menu]\n\n'
helpMsg += '/setmyaddress [set the address `/setmyaddress <address>`]\n'
helpMsg += '/setmyfiat [set the fiat base, default USD `/setmyfiat EUR`]\n'
helpMsg += '/myaddress [view the set address]\n'
helpMsg += '/mytotal [your total amount staked]\n'
helpMsg += '/myrank [your current rank]\n'
helpMsg += '/mytier [your current tier]\n'
helpMsg += '/myrewards [your unclaimed rewards]\n'
helpMsg += '/myfiat [your fiat used to convert values]\n'
helpMsg += '[PRIVATE CHAT ONLY]\n\n'
helpMsg += '/totalstakers [total glq stakers]\n'
helpMsg += '/totalstaked [total amount staked]\n'
helpMsg += '/tiers [total staked in each tier]\n'
helpMsg += '/apy [offered apy]\n'
helpMsg += '/top [top 3 stakers]\n'
helpMsg += '/price [get the current price]\n'
helpMsg += '/pricedata [get market]\n'
helpMsg += '/pricedatafull [all price data]\n'
helpMsg += '/websites [list of all graphlinq websites]\n'
helpMsg += '/socials [list of all socials]\n'
helpMsg += '/staking [staking information]\n'
helpMsg += '/documentation [docs link]\n'
helpMsg += '/listings [where to trade GLQ]\n'
helpMsg += '/shortcuts [shortcuts and legacy commands]\n'
helpMsg += '[PUBLIC & PRIVATE CHAT]'

# Private Command Response In Public Chat
privateMsg = 'This is a private command. Please interact directly with me by clicking here @GraphLinqBot'

# /websites
websites = [
    ['GraphLinq.LandingPage','Official Homepage', 'https://glq.link/home'],
    ['GraphLinq.AI','GraphLinq Chat, Your Personal Assistant with the Power of OpenAI, Graphlinq Engine, and Speech-to-Text','https://glq.link/ai'],
    ['GraphLinq.Analytics','Powerful visualization and analysis on-chain', 'https://glq.link/analytics'],
    ['GraphLinq.App', 'Main GraphLinq App Interface', 'https://glq.link/app'],
    ['GraphLinq.Chain.Explorer','Explorer for the GraphLinq Chain', 'https://glq.link/explorer'],
    ['GraphLinq.Chain.Status', 'GraphLinq Chain Network Status', 'https://glq.link/network'],
    ['GraphLinq.Documentation','GraphLinq Documentation', 'https://glq.link/docs'], # https://glq.link/documentation https://glq.link/doc
    ['GraphLinq.IDE', 'GraphLinq IDE', 'https://glq.link/ide'],
    ['GraphLinq.MarketPlace', 'GraphLinq MarketPlace', 'https://glq.link/marketplace']
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
    ['Staking Website', 'https://glq.link/staking'],
    ['Staking Instructions', 'https://glq.link/stakingdocs']
]

# /documentation
documentation = [
    ['Documentation','https://glq.link/docs']
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
    ['/pricedata', '/data'],
    ['/documentation', '/docs /doc'],
    ['/pricedatafull', '/pricefull'],
    ['/listings', '/buy /exchanges']
]

# /buy cex
cexListings = [
    ['KuCoin', 'GLQ/USDT', 'GLQChain', 'https://glq.link/kucoinGLQ_USDT'],
    ['KuCoin', 'GLQ/BTC', 'GLQChain', 'https://glq.link/kucoinGLQ_BTC'],
    ['Gate io', 'GLQ/ETH', 'InProgress', 'https://glq.link/gateioGLQ_ETH'],
    ['Gate io', 'GLQ/USDT', 'InProgress', 'https://glq.link/gateioGLQ_USDT'],
    ['Bilaxy', 'GLQ/ETH', 'ETH', 'https://glq.link/bilaxyGLQ_ETH'],
    ['MEXC', 'GLQ/USDT', 'GLQChain/ETH', 'https://glq.link/mexcGLQ_USDT']
]

# /buy dex
dexListings = [
    ['Uniswap v3', 'GLQ/WETH', 'ETH', 'https://glq.link/uniswapv3'],
]

# status websites
status = [
    ['GraphLinq Server Status','https://glq.link/status'],
    ['GraphLinq Chain Status','https://glq.link/network']
]

# Developer Application
apply = "Interested in working for GraphLinq? Apply here: https://docs.google.com/forms/d/e/1FAIpQLScA4-jaONRwltts0EqcWlQ_JMdifVS2x2KSbInrSYtmaNm4RQ/viewform"


#### CONT
# Network connection to your node or an infura like service
network_url = 'https://glq-dataseed.graphlinq.io/'
logging.info('[VARIABLE] Network URL: {}' .format(network_url))

# Set the contract address
address = '0xC09062656C4715085d7D345B25a8D8A7ee477521'
logging.info('[VARIABLE] Contract Address: {}' .format(address))

# Load the abi
web3 = Web3(Web3.HTTPProvider(network_url))
abi = json.loads('[{"inputs":[{"internalType":"address","name":"glqAddr","type":"address"},{"internalType":"address","name":"manager","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"staker_address","type":"address"},{"indexed":false,"internalType":"uint256","name":"at_block","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount_registered","type":"uint256"}],"name":"NewStakerRegistered","type":"event"},{"inputs":[{"internalType":"uint256","name":"glqAmount","type":"uint256"}],"name":"addIncentive","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"claimGlq","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"glqAmount","type":"uint256"}],"name":"depositGlq","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"emergencyWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"wallet","type":"address"}],"name":"getDepositedGLQ","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"wallet","type":"address"}],"name":"getGlqToClaim","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"wallet","type":"address"}],"name":"getPosition","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tier","type":"uint256"}],"name":"getTierTotalStaked","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getTiersAPY","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getTopStakers","outputs":[{"internalType":"address[]","name":"","type":"address[]"},{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getTotalIncentive","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getTotalStaked","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getTotalStakers","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"wallet","type":"address"}],"name":"getWaitingPercentAPR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"wallet","type":"address"}],"name":"getWalletCurrentTier","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"glqAmount","type":"uint256"}],"name":"removeIncentive","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"t1","type":"uint256"},{"internalType":"uint256","name":"t2","type":"uint256"},{"internalType":"uint256","name":"t3","type":"uint256"}],"name":"setApyPercentRewards","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"blocks","type":"uint256"}],"name":"setBlocksPerYear","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"state","type":"bool"}],"name":"setEmergencyWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"withdrawGlq","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
logging.info('[VARIABLE] Load abi for: {}' .format(address))

# Set the contract variable
contract = web3.eth.contract(address=address, abi=abi)
logging.info('[VARIABLE] Contract Variable Set: {}' .format(address))


