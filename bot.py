#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File            : bot.py
Author          : GraphLinq Chain
Email           : info@graphlinq.io
Website         : https://graphlinq.io
Repository      : https://github.com/jrbgit/GraphLinq.TelegramBot
Date            : 2023-06-20
Version         : 1.2
Description     : Telegram bot for GraphLinq
"""

# Main Import Block
import os
import re
import time
import platform
import psutil
import socket
import threading
import json
import sqlite3
import requests
from decimal import Decimal
from datetime import datetime, timedelta
from prettytable import PrettyTable
from telegram.ext import Updater, CommandHandler
from eth_utils.address import is_address
from config_logging import (logging, log_formats, log_info, log_warning, log_debug,
                            log_error, log_critical)
from config_maint import (maint_mode, maint_mode_msg, allowed_admin, maint_mode_log_msg_on,
    maint_mode_log_msg_off)
from config_msgs import (version_msg, sheduler_start_msg,start_msg, help_msg_private, help_msg_public,
    private_msg, websites, socials, staking, shortcuts, cex_listings, dex_listings,status,
    set_address_msg,apply)
from config_base import (bot_version, lcw_url, lcw_fiats_url, telegram, lcw_api_key, hub_url)
from config_contract import (contract, web3)
from web3.exceptions import ContractLogicError
from requests.exceptions import RequestException

##########     INITIAL  FUNCTIONS    ##########

def start(update, context):
    """Start the Bot when user first interacts with the bot"""
    log_debug('[STARTING] /start:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        try:
            table = PrettyTable()
            table.field_names = ["GraphLinq Telegram Bot v1.1"]
            for starts in start_msg:
                table.add_row(starts)
            response = '```\n{}```'.format(table.get_string())
            update.message.reply_text(response, parse_mode='Markdown')
            log_debug('[RESPONSE] /start:{} sent: /start' .format(update.message.chat_id))
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /start')
            log_warning('[TRYERROR] /start:{} usage: /start' .format(update.message.chat_id))
    log_debug('[COMPLETE] /start:{}' .format(update.message.chat_id))

def get_help(update, context):
    """Help menu"""
    log_debug('[STARTING] /help:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        try:
            table = PrettyTable()
            table.align = "l"
            table.field_names = ["Public Commands", "Description"]
            for help_public in help_msg_public:
                table.add_row(help_public)
            private = PrettyTable()
            private.align = "l"
            private.field_names = ["Private Commands", "Description"]
            for help_private in help_msg_private:
                private.add_row(help_private)
            response = '```\n{}\n{}```'.format(table.get_string(), private.get_string())
            update.message.reply_text(response, parse_mode='Markdown')
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /help')
            log_warning('[TRYERROR] /help:{} usage: /help' .format(update.message.chat_id))
    log_debug('[COMPLETE] /help:{}' .format(update.message.chat_id))

###########     SETTER FUNCTIONS    ###########

def set_my_address(update, context):
    """Set My Address"""
    log_debug('[STARTING] /setmyaddress:{}'.format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        log_debug('[DATABASE] /setmyaddress:{} lookup user'.format(update.message.chat_id))
        try:
            my_address = context.args[0]
            if is_address(my_address):
                log_debug('[STARTING] /setmyaddress:{} valid address'
                                .format(update.message.chat_id))
                connection = sqlite3.connect("bot.db")
                cursor = connection.cursor()
                cursor.execute("SELECT address FROM users WHERE chat_id = ?",
                            (update.message.chat_id,))
                row = cursor.fetchone()
                if row is None:
                    log_debug('[DATABASE] /setmyaddress:{} insert address into database'
                            .format(update.message.chat_id))
                    cursor.execute("INSERT INTO users (chat_id, address) VALUES (?, ?)",(
                        update.message.chat_id, my_address,))
                    connection.commit()
                    update.message.reply_text('New address set: {}'.format(my_address))
                    log_debug('[DATABASE] /setaddress:{} record {} added'.format(
                        update.message.chat_id, my_address))
                else:
                    if row[0] == my_address:
                        update.message.reply_text('Address is the same...')
                        log_debug('[RESPONSE] /setmyaddress:{} address is the same...'.format(
                            update.message.chat_id))
                    else:
                        cursor.execute("UPDATE users SET address = ? WHERE chat_id = ?", (
                            my_address, update.message.chat_id,))
                        connection.commit()
                        update.message.reply_text('Updated address to: {}'.format(my_address))
                        log_debug('[RESPONSE] /setmyaddress:{} address changed to {}'.format(
                            update.message.chat_id, my_address))
                connection.close()
            else:
                update.message.reply_text('Invalid address...')
                log_debug('[RESPONSE] /setmyaddress:{} invalid address {}'.format(
                    update.message.chat_id, my_address))
        except (IndexError, ValueError):
            log_warning('[TRYERROR] /setmyaddress:{} please provide your address...'.format(
                update.message.chat_id))
            update.message.reply_text('Please provide your address...')
    log_debug('[COMPLETE] /setmyaddress:{}'.format(update.message.chat_id))

#########     MY GETTER FUNCTIONS    ##########

def get_my_address(update, context):
    """Get My Address"""
    log_debug('[STARTING] /myaddress:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        if update.message.chat_id > 0:
            log_debug('[DATABASE] /myaddress:{} lookup address' .format(
                update.message.chat_id))
            try:
                connection = sqlite3.connect("bot.db")
                cursor = connection.cursor()
                cursor.execute("SELECT address FROM users WHERE chat_id = ?",(
                    update.message.chat_id,))
                row = cursor.fetchone()
                if row is None:
                    update.message.reply_text('No address found. Use /setmyaddress first')
                    log_debug('[RESPONSE] /myaddress:{} no address found' .format(
                        update.message.chat_id))
                else:
                    update.message.reply_text('Address: {}'.format(row[0]))
                    log_debug('[RESPONSE] /myaddress:{} db address: {}' .format(
                        update.message.chat_id, row[0]))
                connection.close()
            except (IndexError, ValueError):
                update.message.reply_text('Usage: /myaddress')
                log_warning('[TRYERROR] /myaddress:{} invalid address' .format(
                    update.message.chat_id))
        else:
            update.message.reply_text(private_msg)
            log_debug('[RESPONSE] /myaddress:{} {}' .format(
                update.message.chat_id, private_msg))
    log_debug('[COMPLETE] /myaddress:{}' .format(update.message.chat_id))

def get_my_rank(update, context):
    """Get My Rank"""
    log_debug('[STARTING] /myrank:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False and update.message.chat_id > 0:
        log_debug('[DATABASE] /myrank:{} get address from database' .format(
            update.message.chat_id))
        connection = sqlite3.connect("bot.db")
        cursor = connection.cursor()
        row = cursor.execute(
            "SELECT address FROM users WHERE chat_id = ?",
            (update.message.chat_id,),
        ).fetchone()
        if row is None:
            update.message.reply_text(set_address_msg)
            log_debug('[DATABASE] /myrank:{} get address from database' .format(
                update.message.chat_id))
        else:
            my_address = row[0]
            log_debug('[DATABASE] /myrank:{} matched address {}' .format(
                update.message.chat_id, my_address))
            try:
                if is_address(my_address):
                    user_total = contract.functions.getPosition(my_address).call()
                    text = 'Rank: {}'
                    if user_total > 0:
                        update.message.reply_text(text .format(user_total))
                        log_debug('[RESPONSE] /myrank:{} user {} is ranked {}'
                                    .format(update.message.chat_id, my_address, user_total))
                    else:
                        update.message.reply_text("This address does not have a rank.")
                        log_debug('[RESPONSE] /myrank:{} user {} has no rank {}' .format(
                            update.message.chat_id, my_address, user_total))
                    connection.close()
                else:
                    update.message.reply_text('Address is invalid..')
                    log_debug('[RESPONSE] /myrank:{} address is invalid...'
                                .format(update.message.chat_id))
            except (IndexError, ValueError):
                update.message.reply_text('Usage: /myrank requires /setmyaddress')
                log_warning('[TRYERROR] /myrank:{} requires /setmyaddress'
                            .format(update.message.chat_id))
    else:
        update.message.reply_text(private_msg)
        log_debug('[RESPONSE] /myrank:{} {}'.format(update.message.chat_id, private_msg))
    log_debug('[COMPLETE] /myrank:{}' .format(update.message.chat_id))

def get_my_rewards(update, context):
    """Get the user's rewards"""
    log_debug('[STARTING] /myrewards:{}'.format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        if update.message.chat_id > 0:
            log_debug('[DATABASE] /myrewards:{} get address from database' .format(
                update.message.chat_id))
            connection = sqlite3.connect("bot.db")
            cursor = connection.cursor()
            row = cursor.execute(
                "SELECT address FROM users WHERE chat_id = ?",
                (update.message.chat_id,),
            ).fetchone()
            if row is None:
                update.message.reply_text(set_address_msg)
                log_debug('[DATABASE] /myrewards:{} no match'.format(update.message.chat_id))
            else:
                my_address = row[0]
                log_debug('[DATABASE] /myrewards:{} matched address {}' .format(
                    update.message.chat_id, my_address))
                try:
                    if is_address(my_address):
                        log_debug('[HUBQUERY] /myrewards:{} {}' .format(
                            update.message.chat_id, hub_url))
                        response = get_hub_price(update, context)
                        rate = Decimal(response)
                        user_total = contract.functions.getGlqToClaim(my_address).call()
                        user_in_wei = web3.fromWei(user_total, 'ether')
                        eth_format = ("{:,.2f}".format(user_in_wei))
                        u_total = user_in_wei * rate
                        f_total = ("{:,.2f}".format(u_total))
                        text = 'Unclaimed rewards: {} GLQ || Value ≈ ${}'
                        update.message.reply_text(text .format(eth_format, f_total))
                        log_debug('[RESPONSE] /myrewards:{} user rewards {} ≈ {}'
                                    .format(update.message.chat_id, eth_format, f_total))
                        connection.close()
                    else:
                        log_warning('[RESPONSE] /myrewards:{} address is invalid...'
                                        .format(update.message.chat_id))
                        update.message.reply_text('Address is invalid..')
                except (IndexError, ValueError):
                    update.message.reply_text('There are no rewards at this address.')
                    log_debug('[TRYERROR] /myrewards:{} no rewards at this address'
                                .format(update.message.chat_id))
        else:
            update.message.reply_text(private_msg)
            log_debug('[RESPONSE] {}'.format(private_msg))
    log_debug('[COMPLETE] /myrewards:{}'.format(update.message.chat_id))

def get_my_tier(update, context):
    """Get users tier"""
    log_debug('[STARTING] /mytier:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        if update.message.chat_id > 0:
            log_debug('[DATABASE] /mytier:{} get address from database' .format(
                update.message.chat_id))
            connection = sqlite3.connect("bot.db")
            cursor = connection.cursor()
            row = cursor.execute(
                "SELECT address FROM users WHERE chat_id = ?",
                (update.message.chat_id,),
            ).fetchone()
            if row is None:
                log_debug('[DATABASE] /mytier:{} no match' .format(update.message.chat_id))
                update.message.reply_text('/setaddress must be set first.')
            else:
                my_address = row[0]
                log_debug('[DATABASE] /mytier:{} matched address {}'
                            .format(update.message.chat_id, my_address))
                try:
                    if is_address(my_address):
                        user_total = contract.functions.getWalletCurrentTier(my_address).call()
                        text = 'You are in tier: {}'
                        update.message.reply_text(text .format(user_total))
                        log_debug('[RESPONSE] /mytier:{} user in tier {}' .format(
                            update.message.chat_id, user_total))
                        connection.close()
                    else:
                        update.message.reply_text('Address is invalid...')
                        log_debug('[RESPONSE] /mytier:{} address is invalid...'
                                    .format(update.message.chat_id))
                except (IndexError, ValueError):
                    update.message.reply_text('This address has no tier.')
                    log_warning('[TRYERROR] /mytier:{} address has no tier'.format(
                        update.message.chat_id))
        else:
            update.message.reply_text(private_msg)
            log_debug('[RESPONSE] /mytier:{} {}'.format(update.message.chat_id, private_msg))
    log_debug('[COMPLETE] /mytier:{}'.format(update.message.chat_id))

def get_my_total(update, context):
    """Total Staked"""
    log_debug('[STARTING] /mytotal:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        if update.message.chat_id > 0:
            log_debug('[DATABASE] /mytotal:{} get user address from database' .format(
                update.message.chat_id))
            connection = sqlite3.connect("bot.db")
            cursor = connection.cursor()
            row = cursor.execute(
                "SELECT address FROM users WHERE chat_id = ?",
                (update.message.chat_id,),
            ).fetchone()
            if row is None:
                log_debug('[DATABASE] /mytotal:{} address not set' .format(
                    update.message.chat_id))
                update.message.reply_text("You must first use /setaddress")
            else:
                address = row[0]
                try:
                    if is_address(address):
                        log_debug('[HUBQUERY] /mytotal:{} {}' .format(
                            update.message.chat_id, hub_url))
                        response = get_hub_price(update, context)
                        rate = Decimal(response)
                        user_total = contract.functions.getDepositedGLQ(address).call()
                        user_in_wei = web3.fromWei(user_total, 'ether')
                        u_total = user_in_wei * rate
                        f_total = ("{:,.2f}".format(u_total))
                        eth_format = ("{:,.2f}".format(user_in_wei))
                        #ethFormat = f"{userInWei:,}"
                        text = "You are staking: {} GLQ || Value ≈ ${}"
                        update.message.reply_text(text .format(eth_format, f_total))
                        log_debug("""[RESPONSE] /mytotal:{} user is staking: {} GLQ || Value ≈
                                    ${}""" .format(update.message.chat_id, eth_format, f_total))
                        connection.close()
                    else:
                        update.message.reply_text('Address is invalid...')
                        log_debug('[RESPONSE] /mytotal:{} Addess is invalid...'
                                    .format(update.message.chat_id))
                except (IndexError, ValueError):
                    update.message.reply_text('Usage: /total after you /set your address')
                    log_warning('[TRYERROR] /mytotal:{} Usage: /total after /set'
                                .format(update.message.chat_id))
        else:
            update.message.reply_text(private_msg)
            log_debug('[RESPONSE] /mytotal:{} {}'.format(update.message.chat_id, private_msg))
    log_debug('[COMPLETE] /mytotal:{}' .format(update.message.chat_id))

########     MAIN GETTER FUNCTIONS    #########

def get_apy(update, context):
    """APYs"""
    log_debug('[STARTING] /apy:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        log_debug('[CONTRACT] /apy:{} getTiersAPY' .format(update.message.chat_id))
        apys = contract.functions.getTiersAPY().call()
        tiers_apy = [web3.fromWei(apy, 'ether') for apy in apys]

        table = PrettyTable()
        table.align = "l"
        table.field_names = ['Tier', 'APY']
        table.align["APY"] = "r"
        table.add_row(['Tier 1', '{}%'.format(tiers_apy[0])])
        table.add_row(['Tier 2', '{}%'.format(tiers_apy[1])])
        table.add_row(['Tier 3', '{}%'.format(tiers_apy[2])])

        response = '```\n{}```'.format(table.get_string())
        update.message.reply_text(response, parse_mode='Markdown')
        log_debug('[RESPONSE] /apy:{} Tier 1: {}% Tier 2: {}% Tier 3: {}%'
                    .format(update.message.chat_id, tiers_apy[0], tiers_apy[1], tiers_apy[2]))
    log_debug('[COMPLETE] /apy:{}' .format(update.message.chat_id))

def get_tiers(update, context):
    """Get Tiers"""
    log_debug('[STARTING] /tiers:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        tier_totals = get_tier_totals()
        formatted_tiers = format_tiers(tier_totals)
        send_tiers_response(update, formatted_tiers)
        log_debug('[RESPONSE] /tiers:{}' .format(update.message.chat_id))
    log_debug('[COMPLETE] /tiers:{}' .format(update.message.chat_id))

def get_tier_totals():
    """Get tier totals"""
    total_tier1 = contract.functions.getTierTotalStaked(1).call()
    total_tier2 = contract.functions.getTierTotalStaked(2).call()
    total_tier3 = contract.functions.getTierTotalStaked(3).call()
    return total_tier1, total_tier2, total_tier3

def format_tiers(tier_totals):
    """Format tier totals"""
    tier1_in_wei = web3.fromWei(tier_totals[0], 'ether')
    tier2_in_wei = web3.fromWei(tier_totals[1], 'ether')
    tier3_in_wei = web3.fromWei(tier_totals[2], 'ether')
    staked_t = tier1_in_wei + tier2_in_wei + tier3_in_wei
    formatted_tiers = [
        "{:,.0f}".format(tier1_in_wei),
        "{:,.0f}".format(tier2_in_wei),
        "{:,.0f}".format(tier3_in_wei),
        "{:,.0f}".format(staked_t)
    ]
    return formatted_tiers

def send_price_data_response(update, formatted_tiers):
    """Send response for price data"""
    update.message.reply_text(
        "Tier 1: {} GLQ\n"
        "Tier 2: {} GLQ\n"
        "Tier 3: {} GLQ\n"
        "Total Staked: {} GLQ\n"
        "Total Value: ${}".format(*formatted_tiers)
    )

def send_tiers_response(update, formatted_tiers):
    """Send response for tiers"""
    table = PrettyTable()
    table.align = "l"
    table.field_names = ['Tier', 'Amount (GLQ)']
    table.align["APY"] = "r"
    table.add_row(['Tier 1', '{}'.format(formatted_tiers[0])])
    table.add_row(['Tier 2', '{}'.format(formatted_tiers[1])])
    table.add_row(['Tier 3', '{}'.format(formatted_tiers[2])])
    table.add_row(['--------', '------------'])
    table.add_row(['Total', '{}'.format(formatted_tiers[3])])

    response = '```\n{}```'.format(table.get_string())
    update.message.reply_text(response, parse_mode='Markdown')

def get_top(update, context):
    """Top Stakers"""
    log_debug('[STARTING] /top:{}'.format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        try:
            update.message.reply_text('Usage: /top is disabled')
            log_debug('[RESPONSE] /top:{}'.format(update.message.chat_id))
        except Exception as e:
            log_error(f"Error occurred in /top: {str(e)}")
    log_debug('[COMPLETE] /top:{}'.format(update.message.chat_id))

def format_top_stakers(tops):
    """Format top stakers"""
    top_three = []
    for top in tops:
        top_three.append(top)
    formatted_top_three = [
        re.sub(r'^(.{4}).*(.{4})$', '\\g<1>...\\g<2>', top_three[0][0]),
        re.sub(r'^(.{4}).*(.{4})$', '\\g<1>...\\g<2>', top_three[0][1]),
        re.sub(r'^(.{4}).*(.{4})$', '\\g<1>...\\g<2>', top_three[0][2])
    ]
    return formatted_top_three

def format_staker_values(tops):
    """Format staker values"""
    unformatted_values = [
        web3.fromWei(top, 'ether') for top in tops[1][:3]
    ]
    formatted_values = ["{:,}".format(int(value)).replace(",", "") for value in unformatted_values]
    formatted_values = [float(value) for value in formatted_values]
    return formatted_values

def send_top_stakers_response(update, formatted_top_three, formatted_values, rate):
    """Send response for top stakers"""
    message = "Top Stakers:\n"
    table = PrettyTable()
    table.align = "r"
    table.field_names = ['#', 'Wallet', 'Staked', 'Value']
    for i, value in enumerate(formatted_values, start=1):
        address = formatted_top_three[i - 1]
        value = int(value)
        estimated_value = value * rate
        formatted_value = "{:,}".format(value)
        formatted_estimated_value = "${:,.2f}".format(estimated_value)
        message += f"{i}: {address} ({formatted_value}, {formatted_estimated_value})\n"
        table.add_row([i, address, formatted_value, formatted_estimated_value])
    response = '```\n{}```'.format(table.get_string())
    update.message.reply_text(response, parse_mode='Markdown')

def get_total_staked(update, context):
    """Staked"""
    log_debug('[STARTING] /totalstaked:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        log_debug('[HUBQUERY] /totalstaked:{} {}' .format(update.message.chat_id, hub_url))
        try:
            response = get_hub_price(update, context)
            rate = Decimal(response)
            total_tier1 = contract.functions.getTierTotalStaked(1).call()
            total_tier2 = contract.functions.getTierTotalStaked(2).call()
            total_tier3 = contract.functions.getTierTotalStaked(3).call()
            tier1_in_wei = web3.fromWei(total_tier1, 'ether')
            tier2_in_wei = web3.fromWei(total_tier2, 'ether')
            tier3_in_wei = web3.fromWei(total_tier3, 'ether')
            staked_t = tier1_in_wei + tier2_in_wei + tier3_in_wei
            u_total = staked_t * rate
            f_total = ("{:,.2f}".format(u_total))
            eth_format = ("{:,.2f}".format(staked_t))
            table = PrettyTable()
            table.field_names = ['Staked GLQ', 'Value']
            table.add_row([eth_format, '$' + f_total])
            response = '```\n{}```'.format(table.get_string())
            update.message.reply_text(response, parse_mode='Markdown')
            log_debug('[RESPONSE] /totalstaked:{} Staked GLQ: {} || Value ≈ ${}'
                        .format(update.message.chat_id, eth_format, f_total))
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /totalstaked')
            log_debug('[RESPONSE] /totalstaked:{} usage /totalstaked')
    log_debug('[COMPLETE] /totalstaked:{}' .format(update.message.chat_id))

def get_total_stakers(update, context):
    """Stakers"""
    log_debug('[STARTING] /totalstakers:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        log_debug('[CONTRACT] /totalstakers:{} getTotalStakers' .format(update.message.chat_id))
        try:
            user_total = contract.functions.getTotalStakers().call()
            table = PrettyTable()
            table.field_names = ['Total Stakers']
            table.add_row([user_total])
            response = '```\n{}```'.format(table.get_string())
            update.message.reply_text(response, parse_mode='Markdown')
            log_debug('[RESPONSE] /totalstakers:{} totalStakers:{}'
                        .format(update.message.chat_id, user_total))
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /stakers')
            log_debug('[RESPONSE] /totalstakers:{} usage: /stakers' .format(
                update.message.chat_id))
    log_debug('[COMPLETE] /totalstakers:{}' .format(update.message.chat_id))

#########     LIST FUNCTIONS    ##########

def get_websites(update, context):
    """Websites"""
    log_debug('[STARTING] /websites:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        try:
            response = ''
            for website in websites:
                response += website[0] + ' : ' + website[1] + '\n'
            update.message.reply_text(response)
            log_debug('[RESPONSE] /websites:{} sent websites' .format(update.message.chat_id))
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /websites')
            log_debug('[RESPONSE] /websites:{} usage: /websites' .format(
                update.message.chat_id))
    log_debug('[COMPLETE] /websites:{}' .format(update.message.chat_id))

def get_socials(update, context):
    """Socials"""
    log_debug('[STARTING] /socials:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        try:
            response = ''
            for social in socials:
                response += social[0] + ' : ' + social[1] + '\n'
            update.message.reply_text(response)
            log_debug('[RESPONSE] /socials:{} sent socials' .format(update.message.chat_id))
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /socials')
            log_debug('[RESPONSE] /socials:{} usage: /socials' .format(update.message.chat_id))
    log_debug('[COMPLETE] /socials:{}' .format(update.message.chat_id))

def get_staking(update, context):
    """Staking debug"""
    log_debug('[STARTING] /staking:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        try:
            response = ''
            for stake in staking:
                response += stake[0] + ' : ' + stake[1] + '\n'
            update.message.reply_text(response)
            log_debug('[RESPONSE] /staking:{} sent staking' .format(update.message.chat_id))
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /staking')
            log_debug('[RESPONSE] /staking:{} usage: /staking' .format(update.message.chat_id))
    log_debug('[COMPLETE] /staking:{}' .format(update.message.chat_id))

def get_documentation(update, context):
    """Documentation debug"""
    log_debug('[STARTING] /documentation:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        try:
            response = 'Docs : https://glq.link/docs'
            update.message.reply_text(response)
            log_debug('[RESPONSE] /documentation:{} sent documentation' .format(
                update.message.chat_id))
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /documentation')
            log_debug('[RESPONSE] /documentation:{} usage: /documentation' .format(
                update.message.chat_id))
    log_debug('[COMPLETE] /documentation:{}' .format(update.message.chat_id))

def get_short_cuts(update, context):
    """Shortcuts debug"""
    log_debug('[STARTING] /shortcuts:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        try:
            table = PrettyTable()
            table.align = "l"
            table.field_names = ["Command", "Shortcut"]
            for shortcut in shortcuts:
                table.add_row(shortcut)
            response = '```\n{}```'.format(table.get_string())
            update.message.reply_text(response, parse_mode='Markdown')
            log_debug('[RESPONSE] /shortcuts:{} sent shortcuts' .format(update.message.chat_id))
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /socials')
            log_debug('[RESPONSE] /shortcuts:{} usage: /shortcuts' .format(
                update.message.chat_id))
    log_debug('[COMPLETE] /shortcuts:{}' .format(update.message.chat_id))

def get_listings(update, context):
    """CEX/DEX Listings"""
    log_debug('[STARTING] /listings:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        try:
            response = ''
            for cex_listing in cex_listings:
                response += cex_listing[0] + ' : ' + cex_listing[1] + ' : ' + cex_listing[2] +'\n'
            for dex_listing in dex_listings:
                response += dex_listing[0] + ' : ' + dex_listing[1] + ' : ' + dex_listing[2] +'\n'
            update.message.reply_text(response)
            log_debug('[RESPONSE] /listings:{} sent listings' .format(update.message.chat_id))
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /listings')
            log_debug('[RESPONSE] /listings:{} usage: /listings' .format(
                update.message.chat_id))
    log_debug('[COMPLETE] /listings:{}' .format(update.message.chat_id))

def get_status(update, context):
    """Monitor Status"""
    log_debug('[STARTING] /status:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        try:
            response = ''
            for stat in status:
                response += stat[0] + ' : ' + stat[1] + '\n'
            update.message.reply_text(response)
            log_debug('[RESPONSE] /status:{} sent status' .format(update.message.chat_id))
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /status')
            log_debug('[RESPONSE] /status:{} usage: /status' .format(update.message.chat_id))
    log_debug('[COMPLETE] /status:{}' .format(update.message.chat_id))

def get_apply(update, context):
    """Developer Application"""
    log_debug('[STARTING] /apply:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        log_debug('[RESPONSE] /apply:{}' .format(update.message.chat_id))
        update.message.reply_text(apply)
    log_debug('[COMPLETE] /apply:{}' .format(update.message.chat_id))

#######    GRAPHLINQ CHAIN FUNCTIONS    #######

def get_total_supply_formatted(update, context):
    """Fetch total supply data and format it as a pretty table."""
    log_debug('[STARTING] /supply:{}'.format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        try:
            url = "https://api-explorer.graphlinq.io/get-total-supply"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                
                # Convert timestamp to a more human-readable format
                timestamp = datetime.strptime(data['date'], '%Y-%m-%dT%H:%M:%S.%fZ')
                readable_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                
                # Create and populate the table
                table = PrettyTable()
                table.field_names = ["GraphLinq Chain", "Value"]
                table.align = "l"
                table.add_row(["Total Supply", "{:,}".format(int(data["totalSupply"]))])
                table.add_row(["Current Block #", "{:,}".format(int(data['blockNumber']))])
                table.add_row(["GLQ at Genesis", "{:,}".format(int(data["numberOfGLQAtGENESISBLOCK"]))])
                table.add_row(["Rewards Since Genesis", "{:,}".format(int(data["numberOfGLQRewardedSinceGENESISQ"]))])
                table.add_row(["Server Time Stamp", readable_timestamp])
                table.add_row(["Data Source", "explorer.graphlinq.io"])
                
                # Send the table as a response
                response_message = '```\n{}```'.format(table)
                update.message.reply_text(response_message, parse_mode='Markdown')
                log_debug('[RESPONSE] /supply:{} sent table'.format(update.message.chat_id))
            else:
                update.message.reply_text('Failed to fetch data.')
        except Exception as e:
            update.message.reply_text('An error occurred: {}'.format(e))
            log_debug('[ERROR] /supply:{} {}'.format(update.message.chat_id, e))
    log_debug('[COMPLETE] /supply:{}'.format(update.message.chat_id))

#######     LIVECOINWATCH  FUNCTIONS    #######

def get_live_coin_watch(update, context):
    """LiveCoinWatch Fetch"""
    log_debug('[STARTING] /lcwquery:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        log_debug('[LCWQUERY] /lcwquery:{} {}' .format(update.message.chat_id, lcw_url))
        payload = json.dumps({
            "currency": 'USD',
            "code": "GLQ",
            "meta": True
        })
        headers = {
            'content-type': 'application/json',
            'x-api-key': str(lcw_api_key)
        }
        resp_post = requests.request("POST", lcw_url, headers=headers, data=payload)
        resp_json = json.loads(resp_post.text)
        rate_raw = resp_json["rate"]
        rate = ("{:.6f}".format(rate_raw)).strip()
        response = "Price: ${}\nVolume: ${}\nATH: ${}\nMcap: ${}"
        log_debug('[RESPONSE] /lcwquery:{} Price: {}'
                    .format(update.message.chat_id, rate))
        log_debug('[COMPLETE] /lcwquery:{}' .format(update.message.chat_id))
    return resp_json

def live_coin_watch_fiats(update, context):
    """LiveCoinWatch Fiats"""
    log_debug('[STARTING] /lcwfiats:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        log_debug('[LCWQUERY] /lcwfiats:{} {}' .format(update.message.chat_id, lcw_fiats_url))
        payload = '{}'
        headers = {
            'content-type': 'application/json',
            'x-api-key': lcw_api_key
        }
        resp_post = requests.request("POST", lcw_fiats_url, headers=headers, data=payload)
        resp_json = json.loads(resp_post.text)
        response = "Data Fetched"
        log_debug('[RESPONSE] /lcwfiats:{} {}' .format(update.message.chat_id, response))
        log_debug('[COMPLETE] /lcfiats:{}' .format(update.message.chat_id))
    return resp_json

def local_live_coin_watch_fiats():
    """Local Fiats with Synbol"""
    # does not need to check maint mode
    # because any function that can call this has already done so
    connection = sqlite3.connect("bot.db")
    cursor = connection.cursor()
    local_fiats = cursor.execute("SELECT * FROM fiats").fetchall()
    connection.close()
    return local_fiats


########     GRAPHLINQ HUB API FUNCTIONS     ########

def get_hub_price(update, context):
    """GraphLinq Hub Fetch"""
    log_debug('[STARTING] /hubquery:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        log_debug('[HUBQUERY] /hubquery:{} {}' .format(update.message.chat_id, hub_url))
        resp_get = requests.get(hub_url)
        resp_json = json.loads(resp_get.text)
        rate_raw = resp_json["prices"]["GLQ"]
        #rate = ("{:.6f}".format(rate_raw)).strip()
        log_debug('[RESPONSE] /hubquery:{} Price: {}'
                    .format(update.message.chat_id, rate_raw))
        log_debug('[COMPLETE] /hubquery:{}' .format(update.message.chat_id))
    return rate_raw

########     MAINTENANCE  FUNCTIONS    ########

def admin_command(update, context):
    """Admin-only command"""
    log_info(f"[STARTING] /admin for user {update.message.chat_id}")

    try:
        # Server details
        current_time = datetime.now().strftime('%H:%M:%S')
        current_date = datetime.now().strftime('%Y-%m-%d')
        timezone = time.tzname[time.daylight]
        local_time = time.ctime()
        load_avg = os.getloadavg()[0]
        memory_info = psutil.virtual_memory()
        memory_usage = f"{memory_info.used / (1024**2):.2f} MB of {memory_info.total / (1024**2):.2f} MB"
        uptime_seconds = time.time() - psutil.boot_time()
        uptime = str(timedelta(seconds=uptime_seconds))
        python_version = platform.python_version()

        # Server IP Address
        server_ip = socket.gethostbyname(socket.gethostname())

        # Available Disk Space
        disk_usage = psutil.disk_usage('/')
        available_disk = f"{disk_usage.free / (1024**3):.2f} GB of {disk_usage.total / (1024**3):.2f} GB"

        # Number of Active Threads
        active_threads = threading.active_count()

        # CPU Usage
        cpu_usage = f"{psutil.cpu_percent(interval=1)}%"

        # Memory Use in GB
        memory_usage = f"{memory_info.used / (1024**3):.2f} GB of {memory_info.total / (1024**3):.2f} GB"

        # Network Traffic in GB
        net_io = psutil.net_io_counters()
        sent_data = f"{net_io.bytes_sent / (1024**3):.2f} GB"
        recv_data = f"{net_io.bytes_recv / (1024**3):.2f} GB"

        # Swap Memory Use in GB
        swap_info = psutil.swap_memory()
        swap_usage = f"{swap_info.used / (1024**3):.2f} GB of {swap_info.total / (1024**3):.2f} GB"

        num_processes = len(psutil.pids())
        connections = psutil.net_connections()
        established_connections = len([c for c in connections if c.status == 'ESTABLISHED'])
        boot_time = datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')

        # Constructing the table using PrettyTable
        table = PrettyTable()
        table.field_names = ["Metric", "Value"]
        table.add_row(["Current Time", current_time])
        table.add_row(["Current Date", current_date])
        table.add_row(["Timezone", timezone])
        table.add_row(["Local Time", local_time])
        table.add_row(["System Load (1 min avg)", str(load_avg)])
        table.add_row(["Memory Use", memory_usage])
        table.add_row(["Swap Usage", swap_usage])
        table.add_row(["Uptime", uptime])
        table.add_row(["Python Version", python_version])
        table.add_row(["Bot Version", bot_version])  # Assuming bot_version is defined somewhere in your configs
        table.add_row(["Maintenance Mode", "Enabled" if maint_mode else "Disabled"])
        table.add_row(["Server IP", server_ip])
        table.add_row(["Available Disk Space", available_disk])
        table.add_row(["Active Threads", active_threads])
        table.add_row(["Data Sent", sent_data])
        table.add_row(["Data Received", recv_data])
        table.add_row(["CPU Usage", cpu_usage])
        table.add_row(["Processors", num_processes])
        table.add_row(["Network Load", established_connections])
        table.add_row(["Boot Time", boot_time])


        # Check if the user is the admin
        if update.message.chat_id == allowed_admin:
            # Greet the admin
            #update.message.reply_text("Hello, Admin!")
            update.message.reply_text(f"Hello, Admin!\n```\n{table}\n```", parse_mode='Markdown')
            log_info(f"[RESPONSE] /admin for user {update.message.chat_id}: Provided info to admin.")
        else:
            # If the user is not the admin
            update.message.reply_text(f"Hey, nice to meet you!\n```\n{table}\n```", parse_mode='Markdown')
            log_info(f"[RESPONSE] /admin for user {update.message.chat_id}: Provided info to admin.")

    except Exception as e:
        log_error(f"[ERROR] /admin for user {update.message.chat_id}: {str(e)}")
        update.message.reply_text("An error occurred while processing your request. Please try again later.")

    log_info(f"[COMPLETE] /admin for user {update.message.chat_id}")

def get_maint_mode(update, context):
    """Check if maintenance mode is enabled."""
    if context is None:
        log_warning('[DEBUGGER] No context available')
    if maint_mode == 1:
        if update.message.chat_id == allowed_admin:
            #log_debug('[DEBUGGER] Maintenance: ON | Admin Allowed')
            return False
        log_warning('[DEBUGGER] Maintenance: ON | Not Admin')
        update.message.reply_text(maint_mode_msg)
        return True
    #log_debug('[DEBUGGER] Maintenance: OFF')
    return False

def log_maint_mode():
    """Runs at first start to log maintenance mode."""
    if maint_mode == 1:
        log_warning('[DEBUGGER] {}' .format(maint_mode_log_msg_on))
        log_warning('[DEBUGGER] Admin: {}'.format(allowed_admin))
    else:
        log_info('[DEBUGGER] {}' .format(maint_mode_log_msg_off))

################     ROUTES    ################

def public_routes(dispatch):
    """Public Routes"""
    # General Public Routes
    dispatch.add_handler(CommandHandler("start", start))
    dispatch.add_handler(CommandHandler("help", get_help))
    # Public Staking Routes
    dispatch.add_handler(CommandHandler("apy", get_apy))
    dispatch.add_handler(CommandHandler("top", get_top))
    dispatch.add_handler(CommandHandler("tiers", get_tiers))
    dispatch.add_handler(CommandHandler("totalstaked", get_total_staked))
    dispatch.add_handler(CommandHandler("totalstakers", get_total_stakers))
    # Messages
    dispatch.add_handler(CommandHandler("websites", get_websites))
    dispatch.add_handler(CommandHandler("socials", get_socials))
    dispatch.add_handler(CommandHandler("staking", get_staking))
    dispatch.add_handler(CommandHandler("documentation", get_documentation))
    dispatch.add_handler(CommandHandler("shortcuts", get_short_cuts))
    dispatch.add_handler(CommandHandler("listings", get_listings))
    dispatch.add_handler(CommandHandler("status", get_status))
    dispatch.add_handler(CommandHandler("apply", get_apply))
    # GraphLinq Chain
    dispatch.add_handler(CommandHandler("supply", get_total_supply_formatted))

def private_routes(dispatch):
    """Private Routes"""
    # Private Routes Set
    dispatch.add_handler(CommandHandler("setaddress", set_my_address))
    # Private Routes Get
    dispatch.add_handler(CommandHandler("myaddress", get_my_address))
    dispatch.add_handler(CommandHandler("mytotal", get_my_total))
    dispatch.add_handler(CommandHandler("myrank", get_my_rank))
    dispatch.add_handler(CommandHandler("mytier", get_my_tier))
    dispatch.add_handler(CommandHandler("myrewards", get_my_rewards))

def legacy_routes(dispatch):
    """Legacy Routes"""
    dispatch.add_handler(CommandHandler("address", get_my_address))
    dispatch.add_handler(CommandHandler("set", set_my_address))
    dispatch.add_handler(CommandHandler("total", get_my_total))
    dispatch.add_handler(CommandHandler("rewards", get_my_rewards))
    dispatch.add_handler(CommandHandler("rank", get_my_rank))
    dispatch.add_handler(CommandHandler("tier", get_my_tier))
    dispatch.add_handler(CommandHandler("stakers", get_total_stakers))
    dispatch.add_handler(CommandHandler("staked", get_total_staked))

def alt_routes(dispatch):
    """Alt and Hidden"""
    dispatch.add_handler(CommandHandler("doc", get_documentation))
    dispatch.add_handler(CommandHandler("docs", get_documentation))
    dispatch.add_handler(CommandHandler("website", get_websites))
    dispatch.add_handler(CommandHandler("social", get_socials))
    dispatch.add_handler(CommandHandler("shortcut", get_short_cuts))
    dispatch.add_handler(CommandHandler("short", get_short_cuts))
    dispatch.add_handler(CommandHandler("buy", get_listings))
    dispatch.add_handler(CommandHandler("exchanges", get_listings))
    dispatch.add_handler(CommandHandler("setmyaddress", set_my_address))

def admin_routes(dispatch):
    dispatch.add_handler(CommandHandler('hi', admin_command))
    dispatch.add_handler(CommandHandler('test', get_hub_price))

def main():
    """Main"""
    log_info(version_msg + bot_version)
    # Display Maintenance Status
    log_maint_mode()
    # Create the bot
    updater = Updater(telegram, use_context=True)
    dispatch = updater.dispatcher
    # register public and private routes
    public_routes(dispatch)
    private_routes(dispatch)
    legacy_routes(dispatch)
    alt_routes(dispatch)
    admin_routes(dispatch)
    # Start Polling
    log_info(sheduler_start_msg)
    updater.start_polling()
    updater.idle()

# Initialize
if __name__ == '__main__':
    main()
