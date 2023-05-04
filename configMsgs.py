########################################
######      Bot  Reply  Text      ######
import logging

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
