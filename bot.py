from telegram.ext import Updater, CommandHandler, MessageHandler, filters
import datetime
from datetime import timedelta
import json
from web3 import Web3
import requests
import decimal
import locale
import sqlite3
from contextlib import closing
import re
import logging
from eth_utils.address import (
    is_address,
    is_binary_address,
    is_canonical_address,
    is_checksum_address,
    is_checksum_formatted_address,
    is_hex_address,
    is_normalized_address,
    is_same_address,
    to_canonical_address,
    to_checksum_address,
    to_normalized_address,
)

# Logging
from configLogging import *
# Maintenance
from configMaint import *
# Bot Response Messages
from configMsgs import *
# Base Configuration
from configBase import *
# Web3 Configuration
from configContract import *

###############################################
##########     INITIAL  FUNCTIONS    ##########

# Start the Bot Message
def start(update, context):
    chatId = update.message.chat_id
    logging.info('[STARTING] /start:{}' .format(chatId))
    getHelp(update, context)
    logging.info('[COMPLETE] /start:{}' .format(chatId))


# Help Message
def getHelp(update, context):
    chatId = update.message.chat_id
    logging.info('[STARTING] /help:{}' .format(chatId))
    if (getMaintMode(update, context) == False):
        logging.info('[MAINTMSG] /help:{}' .format(chatId))
        update.message.reply_text(helpMsg)
        logging.info('[RESPONSE] /help:{} sent help menu' .format(chatId))
    else:
        logging.info('[MAINTMSG] /help:{}' .format(chatId))
        update.message.reply_text(maintModeMsg)
        logging.info('[MAINTMSG] /help:{}' .format(maintModeMsg))
    logging.info('[COMPLETE] /help:{}' .format(chatId))



###############################################
###########     SETTER FUNCTIONS    ###########

# Set My Address
def setMyAddress(update, context):
    chatId = update.message.chat_id
    logging.info('[STARTING] /setmyaddress:{}' .format(chatId))
    if (getMaintMode(update, context) == False):
        if (chatId > 0):
            logging.info('[DATABASE] /setmyaddress:{} set address in database' .format(chatId))
            try:
                myAddress = context.args[0]
                if (is_address(myAddress)):
                    logging.info('[DATABASE] /setmyaddress{} valid address' .format(chatId))
                    connection = sqlite3.connect("bot.db")
                    cursor = connection.cursor()
                    row = cursor.execute(
                        "SELECT address FROM users WHERE chat_id = ?",
                        (chatId,),
                    ).fetchone()
                    if (row == None):
                        logging.info('[DATABASE] /setmyaddress:{} insert address into database' .format(chatId))
                        cursor.execute(
                            "INSERT INTO users (chatId, address) VALUES (?, ?)",
                            (chatId, myAddress,)
                        )
                        connection.commit()
                        update.message.reply_text('New address set: {}' .format(myAddress))
                        logging.info('[DATABASE] /setaddress:{} record {} added' .format(chatId, myAddress))
                    else:
                        if (row[0] == myAddress):
                            update.message.reply_text('Address is the same...')
                            logging.info('[RESPONSE] /setmyaddress:{} address is the same...' .format(chatId))
                        else:
                            cursor.execute(
                                "UPDATE users SET address = ? WHERE chat_id = ?",
                                (myAddress, chatId,)
                            )
                            connection.commit()
                            update.message.reply_text('Updated address to: {}' .format(row[0]))
                            logging.info('[RESPONSE] /setmyaddress:{} address changed to {}' .format(chatId, myAddress))
                    connection.close()
                else:
                    update.message.reply_text('Invalid address...')
                    logging.info('[RESPONSE] /setmyaddress:{} invalid address {}' .format(chatId, myAddress))
            except (IndexError, ValueError):
                logging.info('[RESPONSE] /setmyaddress:{} please provide your address...' .format(chatId))
                update.message.reply_text('Please provide your address...')
    else:
        update.message.reply_text(maintModeMsg)
    logging.info('[COMPLETE] /setmyaddress:{}' .format(chatId))


# Set My Fiat
def setMyfiat(update, context):
    chatId = update.message.chat_id
    logging.info('[STARTING] /setmyfiat:{}' .format(chatId))
    if (getMaintMode(update, context) == False):
        if (chatId > 0):
            logging.info('[DATABASE] /setmyfiat:{} set address in database' .format(chatId))
            try:
                myfiat = context.args[0]
                if (is_address(myAddress)):
                    logging.info('[DATABASE] /setmyfiat{} valid address' .format(chatId))
                    connection = sqlite3.connect("map.db")
                    cursor = connection.cursor()
                    row = cursor.execute(
                        "SELECT currency FROM users WHERE chat_id = ?",
                        (chatId,),
                    ).fetchone()
                    if (row == None):
                        logging.info('[DATABASE] /setmyfiat:{} insert address into database' .format(chatId))
                        cursor.execute(
                            "INSERT INTO users (chatId, address, currency) VALUES (?, ?, ?)",
                            (chatId, myAddress,)
                        )
                        connection.commit()
                        update.message.reply_text('New address set: {}' .format(myAddress))
                        logging.info('[DATABASE] /setmyfiat:{} record added' .format(chatId))
                    else:
                        if (row[0] == myAddress):
                            update.message.reply_text('Address is the same...')
                            logging.info('[RESPONSE] /setmyfiat:{} address is the same...' .format(chatId))
                        else:
                            cursor.execute(
                                "UPDATE users SET address = ? WHERE chat_id = ?",
                                (myAddress, chatId,)
                            )
                            connection.commit()
                            update.message.reply_text('Updated address to: {}' .format(row[0]))
                            logging.info('[RESPONSE] /setmyfiat:{} address changed to {}' .format(chatId, myAddress))
                    connection.close()
                else:
                    update.message.reply_text('Invalid address...')
                    logging.info('[RESPONSE] /setmyfiat:{} invalid address {}' .format(chatId, myAddress))
            except (IndexError, ValueError):
                logging.info('[RESPONSE] /setmyfiat:{} please provide your address...' .format(chatId))
                update.message.reply_text('Please provide your address...')
    logging.info('[COMPLETE] /setmyaddress:{}' .format(chatId))



###############################################
#########     MY GETTER FUNCTIONS    ##########

# Get My Address
def getMyAddress(update, context):
    chatId = update.message.chat_id
    logging.info('[STARTING] /myAddress:{}' .format(chatId))
    if (getMaintMode(update, context) == False):
        if (chatId > 0):
            logging.info('[DATABASE] /myAddress:{} view address in database' .format(chatId))
            try:
                connection = sqlite3.connect("map.db")
                cursor = connection.cursor()
                row = cursor.execute(
                    "SELECT address FROM users WHERE chat_id = ?",
                    (chatId,),
                ).fetchone()
                if (row == None):
                    update.message.reply_text('No address found. Use /set <address> first')
                    logging.info('[RESPONSE] /myAddress:{} no address found' .format(chatId))
                else:
                    update.message.reply_text('Address: {}\n(use /setaddress <address> or /set <address> to use a different address)' .format(row[0]))
                    logging.info('[RESPONSE] /myAddress:{} address: {}' .format(chatId, row[0]))
                connection.close()
            except (IndexError, ValueError):
                update.message.reply_text('Usage: /address')
                logging.info('[RESPONSE] /myAddress:{} invalid address {}' .format(chatId, myAddress))
        else:
            update.message.reply_text(privateMessage)
            logging.info('[RESPONSE] /myAddress:{} {}' .format(chatId, privateMessage))
    else:
        update.message.reply_text(maintModeMsg)
    logging.info('[COMPLETE] /myAddress:{}' .format(chatId))


# Get My Fiat
def getMyfiat(update, context):
    chatId = update.message.chat_id
    logging.info('[STARTING] /myfiat:{}' .format(chatId))
    if (getMaintMode(update, context) == False):
        if (chatId > 0):
            logging.info('[DATABASE] /myfiat:{} view address in database' .format(chatId))
            try:
                connection = sqlite3.connect("map.db")
                cursor = connection.cursor()
                row = cursor.execute(
                    "SELECT currency FROM users WHERE chat_id = ?",
                    (chatId,),
                ).fetchone()
                if (row == None):
                    update.message.reply_text('No fiat set. Use /setmyfiat <address> first')
                    logging.info('[RESPONSE] /myfiat:{} no address found' .format(chatId))
                else:
                    update.message.reply_text('Address: {} (use /set <address> to use a different address' .format(row[0]))
                    logging.info('[RESPONSE] /myfiat:{} address: {}' .format(chatId, row[0]))
                connection.close()
            except (IndexError, ValueError):
                update.message.reply_text('Usage: /myfiat')
                logging.info('[RESPONSE] /myfiat:{} invalid address {}' .format(chatId, myAddress))
        else:
            update.message.reply_text(privateMessage)
            logging.info('[RESPONSE] /myfiat:{} {}' .format(chatId, privateMessage))
    logging.info('[COMPLETE] /myfiat:{}' .format(chatId))


# Get My APY's
def getMyApy(update, context):
    print("not implemented")


# Get My Rank
def getMyRank(update, context):
    chatId = update.message.chat_id
    logging.info('[STARTING] /myrank:{}' .format(chatId))
    if (getMaintMode(update, context) == False):
        if (chatId > 0):
            logging.info('[DATABASE] /myrank:{} get address from database' .format(chatId))
            connection = sqlite3.connect("map.db")
            cursor = connection.cursor()
            row = cursor.execute(
                "SELECT address FROM users WHERE chat_id = ?",
                (chatId,),
            ).fetchone()
            if (row == None):
                update.message.reply_text(setmsg)
                logging.info('[DATABASE] /myrank:{} get address from database' .format(chatId))
            else:
                myAddress = row[0]
                logging.info('[DATABASE] /myrank:{} matched address {}' .format(chatId, myAddress))
                try:
                    if (is_address(myAddress)):
                        userTotal = contract.functions.getPosition(myAddress).call()
                        text = 'Rank: {}'
                        if userTotal > 0:
                            update.message.reply_text(text .format(userTotal))
                            logging.info('[RESPONSE] /myrank:{} user {} is ranked {}' .format(chatId, myAddress, userTotal))
                        else:
                            update.message.reply_text("This address does not have a rank.")
                            logging.info('[RESPONSE] /myrank:{} user {} has no rank {}' .format(chatId, myAddress, userTotal))
                        connection.close()
                    else:
                        update.message.reply_text('Address is invalid..')
                        logging.info('[RESPONSE] /myrank:{} address is invalid...' .format(chatId))
                except (IndexError, ValueError):
                    update.message.reply_text('Usage: /myrank after you /setaddress your wallet address')
                    logging.info('[RESPONSE] /myrank:{} sage: /myrank after you /setaddress your wallet address' .format(chatId))
        else:
            update.message.reply_text(privateMessage)
            logging.info('[RESPONSE] /myrank:{} {}' .format(chatId, privateMessage))
    else:
        update.message.reply_text(maintModeMsg)
    logging.info('[COMPLETE] /myrank:{}' .format(chatId))


# Get the user's rewards
def getMyRewards(update, context):
    chatId = update.message.chat_id
    logging.info('[STARTING] /myrewards:{}' .format(chatId))
    if (getMaintMode(update, context) == False):
        if (chatId > 0):
            logging.info('[DATABASE] /myrewards:{} get address from database' .format(chatId))
            connection = sqlite3.connect("map.db")
            cursor = connection.cursor()
            row = cursor.execute(
                "SELECT address FROM users WHERE chat_id = ?",
                (chatId,),
            ).fetchone()
            if (row == None):
                update.message.reply_text(setAddressMsg)
                logging.info('[DATABASE] /myrewards:{} no match' .format(chatId))
            else:
                myAddress = row[0]
                logging.info('[DATABASE] /myrewards:{} matched address {}' .format(chatId, myAddress))
                try:
                    if (is_address(myAddress)):
                        logging.info('[LCWQUERY] /myrewards:{} {}' .format(chatId, lcwUrl))
                        response = getLiveCoinWatch(update, context)
                        var9 = response["rate"]
                        userTotal = contract.functions.getGlqToClaim(myAddress).call()
                        userInWei = web3.fromWei(userTotal, 'ether')
                        ethFormat = ("{:,.2f}".format(userInWei))
                        uTotal = float(userInWei) * var9
                        fTotal = ("{:,.2f}".format(uTotal))
                        text = 'Unclaimed rewards: {} GLQ || Value ≈ ${}'
                        update.message.reply_text(text .format(ethFormat, fTotal))
                        logging.info('[RESPONSE] /myrewards:{} user rewards {} ≈ {}' .format(chatId, ethFormat, fTotal))
                        connection.close()
                    else:
                        logging.warning('[RESPONSE] /myrewards:{} address is invalid...' .format(chatId))
                        update.message.reply_text('Address is invalid..')
                except (IndexError, ValueError):
                    update.message.reply_text('There are no rewards at this address.')
                    logging.info('[RESPONSE] /myrewards:{} no rewards at this address' .format(chatId))
        else:
            update.message.reply_text(privateMsg)
            logging.info('[RESPONSE] {}'.format(privateMsg))
    else:
        update.message.reply_text(maintModeMsg)
    logging.info('[COMPLETE] /myrewards:{}' .format(chatId))


# Get users tier
def getMyTier(update, context):
    chatId = update.message.chat_id
    logging.info('[STARTING] /mytier:{}' .format(chatId))
    if (getMaintMode(update, context) == False):
        if (chatId > 0):
            logging.info('[DATABASE] /mytier:{} get address from database' .format(chatId))
            connection = sqlite3.connect("map.db")
            cursor = connection.cursor()
            row = cursor.execute(
                "SELECT address FROM users WHERE chat_id = ?",
                (chatId,),
            ).fetchone()
            if (row == None):
                logging.info('[DATABASE] /mytier:{} no match' .format(chatId))
                update.message.reply_text('You must first use the /setaddress command to store your address. example: /set 0xYourAddressGoesHere')
            else:
                myAddress = row[0]
                logging.info('[DATABASE] /mytier:{} matched address {}' .format(chatId, myAddress))
                try:
                    if (is_address(address)):
                        userTotal = contract.functions.getWalletCurrentTier(myAddress).call()
                        text = 'You are in tier: {}'
                        update.message.reply_text(text .format(userTotal))
                        logging.info('[RESPONSE] /mytier:{} user in tier {}' .format(chatId, userTotal))
                        connection.close()
                    else:
                        update.message.reply_text('Address is invalid...')
                        logging.info('[RESPONSE] /mytier:{} address is invalid...' .format(chatId))
                except (IndexError, ValueError):
                    update.message.reply_text('This address has no tier.')
                    logging.info('[RESPONSE] /mytier:{} address has no tier' .format(chatId))
        else:
            update.message.reply_text(privateMessage)
            logging.info('[RESPONSE] /mytier:{} {}' .format(chatId, privateMessage))
    else:
        update.message.reply_text(maintModeMsg)
    logging.info('[COMPLETE] /mytier:{}' .format(chatId))


# Total Staked
def getMyTotal(update, context):
    chatId = update.message.chat_id
    logging.info('[STARTING] /mytotal:{}' .format(chatId))
    if (getMaintMode(update, context) == False):
        if (chatId > 0):
            logging.info('[DATABASE] /mytotal:{} get user address from database' .format(chatId))
            connection = sqlite3.connect("map.db")
            cursor = connection.cursor()
            row = cursor.execute(
                "SELECT address FROM users WHERE chat_id = ?",
                (chatId,),
            ).fetchone()
            if (row == None):
                logging.info('[DATABASE] /mytotal:{} address not set' .format(chatId))
                update.message.reply_text("You must first use the /set command to store your address. example: /set 0xYourAddressGoesHere")
            else:
                address = row[0]
                try:
                    if (is_address(address)):
                        logging.info('[LCWQUERY] /mytotal:{} {}' .format(chatId, lcwUrl))
                        response = getLiveCoinWatch(update, context)
                        rate = response["rate"]
                        userTotal = contract.functions.getDepositedGLQ(address).call()
                        userInWei = web3.fromWei(userTotal, 'ether')
                        uTotal = float(userInWei) * rate
                        fTotal = ("{:,.2f}".format(uTotal))
                        ethFormat = ("{:,.2f}".format(userInWei))
                        #ethFormat = f"{userInWei:,}"
                        text = "You are staking: {} GLQ || Value ≈ ${}"
                        update.message.reply_text(text .format(ethFormat, fTotal))
                        logging.info('[RESPONSE] /mytotal:{} user is staking: {} GLQ || Value ≈ ${}' .format(chatId, ethFormat, fTotal))
                        connection.close()
                    else:
                        update.message.reply_text('Address is invalid...')
                        logging.info('[RESPONSE] /mytotal:{} Addess is invalid...' .format(chatId))
                except (IndexError, ValueError):
                    update.message.reply_text('Usage: /total after you /set your address')
                    logging.info('[RESPONSE] /mytotal:{} Usage: /total after you /set your address' .format(chatId))
        else:
            update.message.reply_text(privateMsg)
            logging.info('[RESPONSE] /mytotal:{} {}'.format(chatId, privateMsg))
    else:
        update.message.reply_text(maintModeMsg)
    logging.info('[COMPLETE] /mytotal:{}' .format(chatId))



###############################################
########     MAIN GETTER FUNCTIONS    #########


# APYs
def getApy(update, context):
    chatId = update.message.chat_id
    logging.info('[STARTING] /apy:{}' .format(chatId))
    if (getMaintMode(update, context) == False):
        logging.info('[CONTRACT] /apy:{} getTiersAPY' .format(chatId))
        apys = contract.functions.getTiersAPY().call()
        a = []
        for apy in apys:
            tier = web3.fromWei(apy, 'ether')
            a.append(tier)
        response = 'Tier 1: {}%\nTier 2: {}%\nTier 3: {}%' .format(a[0], a[1], a[2])
        update.message.reply_text(response)
        logging.info('[RESPONSE] /apy:{} Tier 1: {}% Tier 2: {}% Tier 3: {}%' .format(chatId, a[0], a[1], a[2]))
    else:
        update.message.reply_text(maintModeMsg)
    logging.info('[COMPLETE] /apy:{}' .format(chatId))


# Price from LCW
def getPrice(update, context):
    chatId = update.message.chat_id
    logging.info('[STARTING] /price:{}' .format(chatId))
    if (getMaintMode(update, context) == False):
        logging.info('[LCWQUERY] /price:{} {}' .format(chatId, lcwUrl))
        response = getLiveCoinWatch(update, context)
        data = response
        rate = data["rate"]
        price = ("{:.6f}".format(rate))
        text = "Price: ${}"
        update.message.reply_text(text .format(price))
        logging.info('[RESPONSE] /price:{} {}' .format(chatId, price))
    else:
        update.message.reply_text(maintModeMsg)
    logging.info('[COMPLETE] /price:{}' .format(chatId))


# Price with meta data from LCW
def getPriceData(update, context):
    chatId = update.message.chat_id
    logging.info('[STARTING] /pricedata:{}' .format(chatId))
    if (getMaintMode(update, context) == False):
        logging.info('[LCWQUERY] /pricedata:{} {}' .format(chatId, lcwUrl))
        response = getLiveCoinWatch(update, context)
        athRaw = response["allTimeHighUSD"]
        rateRaw = response["rate"]
        volRaw = response["volume"]
        mcapRaw = response["cap"]
        rate = ("{:.6f}".format(rateRaw))
        vol = ("{:,}".format(volRaw))
        ath = ("{:.6f}".format(athRaw))
        mcap = ("{:,}".format(mcapRaw))
        response = "Price: ${}\nVolume: ${}\nATH: ${}\nMcap: ${}"
        logging.info('[RESPONSE] /pricedata:{} Price: ${} Volume: ${} ATH: ${} Mcap: ${}' .format(chatId, rate, vol, ath, mcap))
        update.message.reply_text(response .format(rate, vol, ath, mcap))
    else:
        update.message.reply_text(maintModeMsg)
    logging.info('[COMPLETE] /pricedata:{}' .format(chatId))


# Get Price Full Information
def getPriceDataFull(update, context):
    chatId = update.message.chat_id
    logging.info('[STARTING] /pricedatafull:{}' .format(chatId))
    if (getMaintMode(update, context) == False):
        logging.info('[LCWQUERY] /pricedatafull:{} {}' .format(chatId, lcwUrl))
        response = getLiveCoinWatch(update, context)

        age = response["age"]
        rank = response["rank"]
        exchanges = response["exchanges"]
        markets = response["markets"]
        pairs = response["pairs"]
        athRaw = response["allTimeHighUSD"]
        rateRaw = response["rate"]
        volRaw = response["volume"]
        mcapRaw = response["cap"]
        deltaRaw = response["delta"]
        hourRaw = response["delta"]["hour"]
        dayRaw = response["delta"]["day"]
        weekRaw = response["delta"]["week"]
        monthRaw = response["delta"]["month"]
        quarterRaw = response["delta"]["quarter"]
        yearRaw = response["delta"]["year"]

        hourSub = (hourRaw - 1) * 100
        daySub = (dayRaw - 1) * 100
        weekSub = (weekRaw - 1) * 100
        monthSub = (monthRaw - 1) * 100
        quarterSub = (quarterRaw - 1) * 100
        yearSub = (yearRaw - 1) * 100

        hourDelta = str(round(hourSub, 2))
        dayDelta = str(round(daySub, 2))
        weekDelta = str(round(weekSub, 2))
        monthDelta = str(round(monthSub, 2))
        quarterDelta = str(round(quarterSub, 2))
        yearDelta = str(round(yearSub, 2))

        rate = ("{:.6f}".format(rateRaw))
        vol = ("{:,}".format(volRaw))
        ath = ("{:.6f}".format(athRaw))
        mcap = ("{:,}".format(mcapRaw))

        response = "Price: ${} | Volume: ${}\nATH: ${} | Mcap: ${}\n\nHour Delta: {}% | Day Delta: {}%\nWeek Delta: {}% | Month Delta: {}%\nQuarter Delta: {}% | Year Delta: {}%\n\nRank: {} | Exchanges: {}\nMarkets: {} | Pairs: {}\nAge (days): {}"
        respLog = "/pricedatafull:{} Price: ${} | Volume: ${} | ATH: ${} | Mcap: ${} | Hour Delta: {}% | Day Delta: {}% | Week Delta: {}% | Month Delta: {}% | Quarter Delta: {}% | Year Delta: {}% | Rank: {} | Exchanges: {}\nMarkets: {} | Pairs: {} | Age (days): {}"

        logging.info(respLog .format(chatId, rate, vol, ath, mcap, hourDelta, dayDelta, weekDelta, monthDelta, quarterDelta, yearDelta, rank, exchanges, markets, pairs, age))
        update.message.reply_text(response .format(rate, vol, ath, mcap, hourDelta, dayDelta, weekDelta, monthDelta, quarterDelta, yearDelta, rank, exchanges, markets, pairs, age))
    else:
        update.message.reply_text(maintModeMsg)
    logging.info('[COMPLETE] /pricedatafull:{}' .format(chatId))


# Tiers
def getTiers(update, context):
    chatId = update.message.chat_id
    logging.info('[STARTING] /tiers:{}' .format(chatId))
    if (getMaintMode(update, context) == False):
        try:
            logging.info('[LCWQUERY] /tiers:{} {}' .format(chatId, lcwUrl))
            response = getLiveCoinWatch(update, context)
            rate = response["rate"]
            totalTier1 = contract.functions.getTierTotalStaked(1).call()
            totalTier2 = contract.functions.getTierTotalStaked(2).call()
            totalTier3 = contract.functions.getTierTotalStaked(3).call()
            tier1InWei = web3.fromWei(totalTier1, 'ether')
            tier2InWei = web3.fromWei(totalTier2, 'ether')
            tier3InWei = web3.fromWei(totalTier3, 'ether')
            uTotal1 = float(tier1InWei) * rate
            fTotal1 = ("{:,.2f}".format(uTotal1))
            uTotal2 = float(tier2InWei) * rate
            fTotal2 = ("{:,.2f}".format(uTotal2))
            uTotal3 = float(tier3InWei) * rate
            fTotal3 = ("{:,.2f}".format(uTotal3))
            tier1Forma = ("{:,.2f}".format(tier1InWei))
            tier2Forma = ("{:,.2f}".format(tier2InWei))
            tier3Forma = ("{:,.2f}".format(tier3InWei))
            text = 'Total Staked By Tier:\nTier 1: GLQ {} || Value ≈ ${}\nTier 2: GLQ {} || Value ≈ ${}\nTier 3: GLQ {} || Value ≈ ${}'
            update.message.reply_text(text .format(tier1Forma, fTotal1, tier2Forma, fTotal2, tier3Forma, fTotal3))
            logging.info('[RESPONSE] /tiers:{} Total Staked By Tier | Tier 1: GLQ {} || Value ≈ ${} Tier 2: GLQ {} || Value ≈ ${}Tier 3: GLQ {} || Value ≈ ${}' .format(chatId, tier1Forma, fTotal1, tier2Forma, fTotal2, tier3Forma, fTotal3))
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /tiers')
            logging.info('[RESPONSE] /tiers:{} Usage: /tiers' .format(chatId))
    else:
        update.message.reply_text(maintModeMsg)
    logging.info('[COMPLETE] /tiers:{}' .format(chatId))


# Top 3 Stakers
def getTop(update, context):
    chatId = update.message.chat_id
    logging.info('[STARTING] /top:{}' .format(chatId))
    if (getMaintMode(update, context) == False):
        logging.info('[CONTRACT] /top:{} getTopStakers' .format(chatId))
        tops = contract.functions.getTopStakers().call()
        t = []
        for top in tops:
            t.append(top)

        first = re.sub(r'^(.{5}).*(.{5})$', '\g<1>...\g<2>', t[0][0])
        second = re.sub(r'^(.{5}).*(.{5})$', '\g<1>...\g<2>', t[0][1])
        third = re.sub(r'^(.{5}).*(.{5})$', '\g<1>...\g<2>', t[0][2])
        fir = web3.fromWei(t[1][0], 'ether')
        sec = web3.fromWei(t[1][1], 'ether')
        thr = web3.fromWei(t[1][2], 'ether')

        logging.info('[LCWQUERY] /top:{} {}' .format(chatId, lcwUrl))
        response = getLiveCoinWatch(update, context)
        rate = response["rate"]
        convF = ("{:,.2f}".format(fir))
        convS = ("{:,.2f}".format(sec))
        convT = ("{:,.2f}".format(thr))
        ffF = float(fir) * rate
        ffS = float(sec) * rate
        ffT = float(thr) * rate
        fT = ("{:,.2f}".format(ffF))
        sT = ("{:,.2f}".format(ffS))
        tT = ("{:,.2f}".format(ffT))

        response = ('#1 {} || GLQ: {} || Value ≈ ${}\n#2 {} || GLQ: {} || Value ≈ ${}\n#3 {} || GLQ: {} || Value ≈ ${}' .format(first, convF, fT, second, convS, sT, third, convT, tT))
        update.message.reply_text(response)
        logging.info('[RESPONSE] /top:{} #1 {} || GLQ: {} || Value ≈ ${} #2 {} || GLQ: {} || Value ≈ ${} #3 {} || GLQ: {} || Value ≈ ${}' .format(chatId, first, convF, fT, second, convS, sT, third, convT, tT))
    else:
        update.message.reply_text(maintModeMsg)
    logging.info('[COMPLETE] /top:{}' .format(chatId))


# Staked
def getTotalStaked(update, context):
    chatId = update.message.chat_id
    logging.info('[STARTING] /totalstaked:{}' .format(chatId))
    if (getMaintMode(update, context) == False):
        logging.info('[LCWQUERY] /totalstaked:{} {}' .format(chatId, lcwUrl))
        try:
            response = getLiveCoinWatch(update, context)
            rate = response["rate"]
            totalTier1 = contract.functions.getTierTotalStaked(1).call()
            totalTier2 = contract.functions.getTierTotalStaked(2).call()
            totalTier3 = contract.functions.getTierTotalStaked(3).call()
            tier1InWei = web3.fromWei(totalTier1, 'ether')
            tier2InWei = web3.fromWei(totalTier2, 'ether')
            tier3InWei = web3.fromWei(totalTier3, 'ether')
            stakedT = tier1InWei + tier2InWei + tier3InWei
            uTotal = float(stakedT) * rate
            fTotal = ("{:,.2f}".format(uTotal))
            ethFormat = ("{:,.2f}".format(stakedT))
            text = 'Staked GLQ: {} || Value ≈ ${}'
            update.message.reply_text(text .format(ethFormat, fTotal))
            logging.info('[RESPONSE] /totalstaked:{} Staked GLQ: {} || Value ≈ ${}' .format(chatId, ethFormat, fTotal))
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /staked')
            logging.info('[RESPONSE] /totalstaked:{} usage /staked')
    else:
        update.message.reply_text(maintModeMsg)
    logging.info('[COMPLETE] /totalstaked:{}' .format(chatId))


# Stakers
def getTotalStakers(update, context):
    chatId = update.message.chat_id
    logging.info('[STARTING] /totalstakers:{}' .format(chatId))
    if (getMaintMode(update, context) == False):
        logging.info('[CONTRACT] /totalstakers:{} getTotalStakers' .format(chatId))
        try:
            userTotal = contract.functions.getTotalStakers().call()
            text = 'Stakers: {}'
            update.message.reply_text(text .format(userTotal))
            logging.info('[RESPONSE] /totalstakers:{} totalStakers:{}' .format(chatId, userTotal))
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /stakers')
            logging.info('[RESPONSE] /totalstakers:{} usage: /stakers' .format(chatId))
    else:
        update.message.reply_text(maintModeMsg)
    logging.info('[COMPLETE] /totalstakers:{}' .format(chatId))



###############################################
#########     LIST INFO FUNCTIONS    ##########


# Websites
def getWebsites(update, context):
    chatId = update.message.chat_id
    logging.info('[STARTING] /websites:{}' .format(chatId))
    if (getMaintMode(update, context) == False):
        try:
            w = ''
            for website in websites:
                w += ('{}\n{}\n{}\n\n' .format(website[0], website[1], website[2]))
                logging.info('[RESPONSE] /websites:{} {} {} {}' .format(chatId, website[0], website[1], website[2]))
            update.message.reply_text('GRAPHLINQ WEBSITES\n\n{}' .format(w))
            logging.info('[RESPONSE] /websites:{} sent websites' .format(chatId))
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /websites')
            logging.info('[RESPONSE] /websites:{} usage: /websites' .format(chatId))
    else:
        update.message.reply_text(maintModeMsg)
    logging.info('[COMPLETE] /websites:{}' .format(chatId))


# Socials
def getSocials(update, context):
    chatId = update.message.chat_id
    logging.info('[STARTING] /socials:{}' .format(chatId))
    if (getMaintMode(update, context) == False):
        try:
            s = ''
            for social in socials:
                logging.info('[RESPONSE] /socials:{} {} {}' .format(chatId, social[0], social[1]))
                s += ('{}: {}\n' .format(social[0], social[1]))
            update.message.reply_text('SOCIAL MEDIA\n\n{}' .format(s))
            logging.info('[RESPONSE] /socials:{} sent socials' .format(chatId))
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /socials')
            logging.info('[RESPONSE] /socials:{} usage: /socials' .format(chatId))
    else:
        update.message.reply_text(maintModeMsg)
    logging.info('[COMPLETE] /socials:{}' .format(chatId))


# Staking Info
def getStaking(update, context):
    chatId = update.message.chat_id
    logging.info('[STARTING] /staking:{}' .format(chatId))
    if (getMaintMode(update, context) == False):
        try:
            s = ''
            for stake in staking:
                logging.info('[RESPONSE] /staking:{} {} {}' .format(chatId, stake[0], stake[1]))
                s += ('{}: {}\n' .format(stake[0], stake[1]))
            update.message.reply_text('STAKING INFORMATION\n\n{}' .format(s))
            logging.info('[RESPONSE] /staking:{} sent socials' .format(chatId))
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /socials')
            logging.info('[RESPONSE] /staking:{} usage: /staking' .format(chatId))
    else:
        update.message.reply_text(maintModeMsg)
    logging.info('[COMPLETE] /staking:{}' .format(chatId))


# Documentation Info
def getDocumentation(update, context):
    chatId = update.message.chat_id
    logging.info('[STARTING] /documentation:{}' .format(chatId))
    if (getMaintMode(update, context) == False):
        try:
            response = 'https://glq.link/docs'
            update.message.reply_text('DOCUMENTATION\n\n{}' .format(response))
            logging.info('[RESPONSE] /documentation:{} sent documentation' .format(chatId))
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /documentation')
            logging.info('[RESPONSE] /documentation:{} usage: /documentation' .format(chatId))
    else:
        update.message.reply_text(maintModeMsg)
    logging.info('[COMPLETE] /documentation:{}' .format(chatId))


# Shortcuts Info
def getShortCuts(update, context):
    chatId = update.message.chat_id
    logging.info('[STARTING] /shortcuts:{}' .format(chatId))
    if (getMaintMode(update, context) == False):
        try:
            sc = ''
            for shortcut in shortcuts:
                logging.info('[RESPONSE] /shortcuts:{} {} | {}' .format(chatId, shortcut[0], shortcut[1]))
                sc += ('{} | {}\n' .format(shortcut[0], shortcut[1]))
            update.message.reply_text('SHORTCUTS & LEGACY COMMANDS\n\n{}' .format(sc))
            logging.info('[RESPONSE] /shortcuts:{} sent shortcuts' .format(chatId))
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /socials')
            logging.info('[RESPONSE] /shortcuts:{} usage: /shortcuts' .format(chatId))
    else:
        update.message.reply_text(maintModeMsg)
    logging.info('[COMPLETE] /shortcuts:{}' .format(chatId))


# /buy
def getListings(update, context):
    chatId = update.message.chat_id
    logging.info('[STARTING] /listings:{}' .format(chatId))
    if (getMaintMode(update, context) == False):
        try:
            cl = ''
            for cexListing in cexListings:
                logging.info('[RESPONSE] /listings:{} | {}| {} | {} | {}' .format(chatId, cexListing[1], cexListing[0], cexListing[2], cexListing[3]))
                cl += ('{} | {} | {} | {}\n' .format(cexListing[1], cexListing[0], cexListing[2], cexListing[3]))

            dl = ''
            for dexListing in dexListings:
                logging.info('[RESPONSE] /listings:{} | {} | {} | {} | {}' .format(chatId, dexListing[1], dexListing[0], dexListing[2], dexListing[3]))
                dl += ('{} | {} | {} | {}\n' .format(dexListing[1], dexListing[0], dexListing[2], dexListing[3]))

            # send message now here
            response = ('DECENTRALIZED\n\n{}\n\nCENTRALIZED\n\n{}' .format(dl, cl))
            update.message.reply_text('LISTINGS\n\n{}' .format(response))
            logging.info('[RESPONSE] /listings:{} sent listings' .format(chatId))

        except (IndexError, ValueError):
            update.message.reply_text('Usage: /listings')
            logging.info('[RESPONSE] /listings:{} usage: /listings' .format(chatId))
    else:
        update.message.reply_text(maintModeMsg)
    logging.info('[COMPLETE] /listings:{}' .format(chatId))


# Monitoring Info /status
def getStatus(update, context):
    chatId = update.message.chat_id
    logging.info('[STARTING] /status:{}' .format(chatId))
    if (getMaintMode(update, context) == False):
        try:
            st = ''
            for stat in status:
                logging.info('[RESPONSE] /status:{} {} | {}' .format(chatId, stat[0], stat[1]))
                st += ('{} | {}\n' .format(stat[0], stat[1]))
            update.message.reply_text('GRAPHLINQ STATUS\n\n{}' .format(st))
            logging.info('[RESPONSE] /status:{} sent status' .format(chatId))
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /status')
            logging.info('[RESPONSE] /status:{} usage: /status' .format(chatId))
    else:
        update.message.reply_text(maintModeMsg)
    logging.info('[COMPLETE] /status:{}' .format(chatId))



###############################################
#######     LIVECOINWATCH  FUNCTIONS    #######

# LiveCoinWatch Fetch
def getLiveCoinWatch(update, context):
    chatId = update.message.chat_id
    logging.info('[STARTING] /lcwquery:{}' .format(chatId))
    if (getMaintMode(update, context) == False):
        logging.info('[LCWQUERY] /lcwquery:{} {}' .format(chatId, lcwUrl))
        payload = json.dumps({
            "currency": "USD",
            "code": "GLQ",
            "meta": True
        })
        headers = {
            'content-type': 'application/json',
            'x-api-key': 'e445bbe9-5a54-4925-a17f-dfb4c36a09fa'
        }
        respPost = requests.request("POST", lcwUrl, headers=headers, data=payload)
        respJson = json.loads(respPost.text)
        athRaw = respJson["allTimeHighUSD"]
        rateRaw = respJson["rate"]
        volRaw = respJson["volume"]
        mcapRaw = respJson["cap"]
        rate = ("{:.6f}".format(rateRaw)).strip()
        vol = ("{:,}".format(volRaw)).strip()
        ath = ("{:.6f}".format(athRaw))
        mcap = ("{:,}".format(mcapRaw))
        response = "Price: ${}\nVolume: ${}\nATH: ${}\nMcap: ${}"
        logging.info('[RESPONSE] /lcwquery:{} Price: ${} Volume: ${} ATH: ${} Mcap: ${}' .format(chatId, rate, vol, ath, mcap))
        logging.info('[COMPLETE] /lcwquery:{}' .format(chatId))
        return respJson
    else:
        update.message.reply_text(maintModeMsg)
    logging.info('[COMPLETE] /lcwquery:{}' .format(chatId))


# LiveCoinWatch Fiats
#def liveCoinWatchFiats:
#    ...



###############################################
########     MAINTENANCE  FUNCTIONS    ########

# Check if maintenance mode is enabled.
def getMaintMode(update, context):
    chatId = update.message.chat_id
    if (maintMode == 1) and (chatId != allowedAdmin):
        return True
    else:
        return False


# Runs at first start to log maintenance mode.
def logMaintMode():
    if (maintMode == 1):
        logging.warning('[USERMODE] {}' .format(maintModeLogMsgOn))
        logging.warning('[USERMODE] Admin: {}'.format(allowedAdmin))
        return
    else:
        logging.warning('[USERMODE] {}' .format(maintModeLogMsgOff))
        return



###############################################
############     MAIN FUNCTIONS    ############

# Main
def main():
    # Display Maintenance Status
    logMaintMode()

    # Create the bot
    updater = Updater(telegram, use_context=True)
    dp = updater.dispatcher

    # General Public Routes
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", getHelp))

    # Private Routes Set
    dp.add_handler(CommandHandler("setaddress", setMyAddress))

    # Private Routes Get
    dp.add_handler(CommandHandler("myaddress", getMyAddress))
    dp.add_handler(CommandHandler("mytotal", getMyTotal))
    dp.add_handler(CommandHandler("myrank", getMyRank))
    dp.add_handler(CommandHandler("mytier", getMyTier))
    dp.add_handler(CommandHandler("myrewards", getMyRewards))

    # Public Routes
    dp.add_handler(CommandHandler("apy", getApy))
    dp.add_handler(CommandHandler("price", getPrice))
    dp.add_handler(CommandHandler("pricedata", getPriceData))
    dp.add_handler(CommandHandler("pricedatafull", getPriceDataFull))
    dp.add_handler(CommandHandler("tiers", getTiers))
    dp.add_handler(CommandHandler("top", getTop))
    dp.add_handler(CommandHandler("totalstaked", getTotalStaked))
    dp.add_handler(CommandHandler("totalstakers", getTotalStakers))
    dp.add_handler(CommandHandler("websites", getWebsites))
    dp.add_handler(CommandHandler("socials", getSocials))
    dp.add_handler(CommandHandler("staking", getStaking))
    dp.add_handler(CommandHandler("documentation", getDocumentation))
    dp.add_handler(CommandHandler("shortcuts", getShortCuts))
    dp.add_handler(CommandHandler("listings", getListings))
    dp.add_handler(CommandHandler("status", getStatus))

    # Legacy Routes
    dp.add_handler(CommandHandler("address", getMyAddress))
    dp.add_handler(CommandHandler("set", setMyAddress))
    dp.add_handler(CommandHandler("total", getMyTotal))
    dp.add_handler(CommandHandler("rewards", getMyRewards))
    dp.add_handler(CommandHandler("rank", getMyRank))
    dp.add_handler(CommandHandler("tier", getMyTier))
    dp.add_handler(CommandHandler("stakers", getTotalStakers))
    dp.add_handler(CommandHandler("staked", getTotalStaked))
    dp.add_handler(CommandHandler("data", getPriceData))

    # Hidden Shortcuts & Alternate Spellings
    dp.add_handler(CommandHandler("doc", getDocumentation))
    dp.add_handler(CommandHandler("docs", getDocumentation))
    dp.add_handler(CommandHandler("pricefull", getPriceDataFull))
    dp.add_handler(CommandHandler("website", getWebsites))
    dp.add_handler(CommandHandler("social", getSocials))
    dp.add_handler(CommandHandler("shortcut", getShortCuts))
    dp.add_handler(CommandHandler("short", getShortCuts))
    dp.add_handler(CommandHandler("buy", getListings))
    dp.add_handler(CommandHandler("exchanges", getListings))
    dp.add_handler(CommandHandler("setmyaddress", setMyAddress))

    # Start Polling
    logging.info('[USERMODE] Starting Scheduler')
    updater.start_polling()
    updater.idle()


# Initialize
if __name__ == '__main__':
    main()
