#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File            : config_contract.py
Author          : GraphLinq Chain
Email           : info@graphlinq.io
Website         : https://graphlinq.io
Repository      : https://github.com/jrbgit/GraphLinq.TelegramBot
Date            : 2023-06-20
Version         : 1.2
Description     : Contract Config - Telegram bot for GraphLinq
"""

# Network to connect to like infura
import logging
import json
from web3 import Web3

from config_logging import (logging, log_formats, log_info, log_warning, log_debug,
                            log_error, log_critical)
from config_msgs import (version_msg, sheduler_start_msg,start_msg, help_msg_private, help_msg_public,
    private_msg, websites, socials, staking, shortcuts, cex_listings, dex_listings,status,
    set_address_msg,apply)
from config_base import (bot_version, lcw_url,lcw_fiats_url,telegram,lcw_api_key)


# Network connection to your node or an infura like service
network_url = 'https://glq-dataseed.graphlinq.io/'
log_info('[SETTINGS] Network URL: {}' .format(network_url))

# Set the contract address
address = '0xC09062656C4715085d7D345B25a8D8A7ee477521'
log_info('[SETTINGS] Contract Address: {}' .format(address))

# Load the abi
web3 = Web3(Web3.HTTPProvider(network_url))
abi = json.loads('[{"inputs":[{"internalType":"address","name":"glqAddr","type":"address"},{"internalType":"address","name":"manager","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"staker_address","type":"address"},{"indexed":false,"internalType":"uint256","name":"at_block","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount_registered","type":"uint256"}],"name":"NewStakerRegistered","type":"event"},{"inputs":[{"internalType":"uint256","name":"glqAmount","type":"uint256"}],"name":"addIncentive","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"claimGlq","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"glqAmount","type":"uint256"}],"name":"depositGlq","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"emergencyWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"wallet","type":"address"}],"name":"getDepositedGLQ","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"wallet","type":"address"}],"name":"getGlqToClaim","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"wallet","type":"address"}],"name":"getPosition","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tier","type":"uint256"}],"name":"getTierTotalStaked","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getTiersAPY","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getTopStakers","outputs":[{"internalType":"address[]","name":"","type":"address[]"},{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getTotalIncentive","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getTotalStaked","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getTotalStakers","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"wallet","type":"address"}],"name":"getWaitingPercentAPR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"wallet","type":"address"}],"name":"getWalletCurrentTier","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"glqAmount","type":"uint256"}],"name":"removeIncentive","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"t1","type":"uint256"},{"internalType":"uint256","name":"t2","type":"uint256"},{"internalType":"uint256","name":"t3","type":"uint256"}],"name":"setApyPercentRewards","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"blocks","type":"uint256"}],"name":"setBlocksPerYear","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"state","type":"bool"}],"name":"setEmergencyWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"withdrawGlq","outputs":[],"stateMutability":"nonpayable","type":"function"}]')
log_info('[SETTINGS] Load abi for: {}' .format(address))

# Set the contract variable
contract = web3.eth.contract(address=address, abi=abi)
log_info('[SETTINGS] Contract Variable Set: {}' .format(address))
