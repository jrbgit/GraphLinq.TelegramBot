#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File            : bot.py
Author          : GraphLinq Chain
Email           : info@graphlinq.io
Website         : https://graphlinq.io
Repository      : https://github.com/jrbgit/GraphLinq.TelegramBot
Date            : 2023-06-20
Version         : 1.1
Description     : Telegram bot for GraphLinq
"""

# Main Import Block
import re
import json
import sqlite3
import requests
from prettytable import PrettyTable
from telegram.ext import Updater, CommandHandler
from eth_utils.address import is_address
from config_logging import (logging)
from config_maint import (maint_mode, maint_mode_msg, allowed_admin, maint_mode_log_msg_on,
    maint_mode_log_msg_off)
from config_msgs import (start_msg, help_msg_private, help_msg_public,
    private_msg, websites, socials, staking, shortcuts, cex_listings, dex_listings,status,
    set_address_msg,apply)
from config_base import (lcw_url,lcw_fiats_url,telegram,lcw_api_key)
from config_contract import (contract, web3)

##########     INITIAL  FUNCTIONS    ##########

def start(update, context):
    """Start the Bot when user first interacts with the bot"""
    logging.info('[STARTING] /start:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        try:
            table = PrettyTable()
            table.field_names = ["GraphLinq Telegram Bot v1.1"]
            for starts in start_msg:
                table.add_row(starts)
            response = '```\n{}```'.format(table.get_string())
            update.message.reply_text(response, parse_mode='Markdown')
            logging.info('[RESPONSE] /start:{} sent: /start' .format(update.message.chat_id))
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /start')
            logging.warning('[TRYERROR] /start:{} usage: /start' .format(update.message.chat_id))
    logging.info('[COMPLETE] /start:{}' .format(update.message.chat_id))

def get_help(update, context):
    """Help menu"""
    logging.info('[STARTING] /help:{}' .format(update.message.chat_id))
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
            logging.warning('[TRYERROR] /help:{} usage: /help' .format(update.message.chat_id))
    logging.info('[COMPLETE] /help:{}' .format(update.message.chat_id))

###########     SETTER FUNCTIONS    ###########

def set_my_address(update, context):
    """Set My Address"""
    logging.info('[STARTING] /setmyaddress:{}'.format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        logging.info('[DATABASE] /setmyaddress:{} lookup user'.format(update.message.chat_id))
        try:
            my_address = context.args[0]
            if is_address(my_address):
                logging.info('[STARTING] /setmyaddress:{} valid address'
                                .format(update.message.chat_id))
                connection = sqlite3.connect("bot.db")
                cursor = connection.cursor()
                cursor.execute("SELECT address FROM users WHERE chat_id = ?",
                            (update.message.chat_id,))
                row = cursor.fetchone()
                if row is None:
                    logging.info('[DATABASE] /setmyaddress:{} insert address into database'
                            .format(update.message.chat_id))
                    cursor.execute("INSERT INTO users (chat_id, address) VALUES (?, ?)",(
                        update.message.chat_id, my_address,))
                    connection.commit()
                    update.message.reply_text('New address set: {}'.format(my_address))
                    logging.info('[DATABASE] /setaddress:{} record {} added'.format(
                        update.message.chat_id, my_address))
                else:
                    if row[0] == my_address:
                        update.message.reply_text('Address is the same...')
                        logging.info('[RESPONSE] /setmyaddress:{} address is the same...'.format(
                            update.message.chat_id))
                    else:
                        cursor.execute("UPDATE users SET address = ? WHERE chat_id = ?", (
                            my_address, update.message.chat_id,))
                        connection.commit()
                        update.message.reply_text('Updated address to: {}'.format(my_address))
                        logging.info('[RESPONSE] /setmyaddress:{} address changed to {}'.format(
                            update.message.chat_id, my_address))
                connection.close()
            else:
                update.message.reply_text('Invalid address...')
                logging.info('[RESPONSE] /setmyaddress:{} invalid address {}'.format(
                    update.message.chat_id, my_address))
        except (IndexError, ValueError):
            logging.warning('[TRYERROR] /setmyaddress:{} please provide your address...'.format(
                update.message.chat_id))
            update.message.reply_text('Please provide your address...')
    logging.info('[COMPLETE] /setmyaddress:{}'.format(update.message.chat_id))

#########     MY GETTER FUNCTIONS    ##########

def get_my_address(update, context):
    """Get My Address"""
    logging.info('[STARTING] /myaddress:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        if update.message.chat_id > 0:
            logging.info('[DATABASE] /myaddress:{} lookup address' .format(
                update.message.chat_id))
            try:
                connection = sqlite3.connect("bot.db")
                cursor = connection.cursor()
                cursor.execute("SELECT address FROM users WHERE chat_id = ?",(
                    update.message.chat_id,))
                row = cursor.fetchone()
                if row is None:
                    update.message.reply_text('No address found. Use /setmyaddress first')
                    logging.info('[RESPONSE] /myaddress:{} no address found' .format(
                        update.message.chat_id))
                else:
                    update.message.reply_text('Address: {}'.format(row[0]))
                    logging.info('[RESPONSE] /myaddress:{} db address: {}' .format(
                        update.message.chat_id, row[0]))
                connection.close()
            except (IndexError, ValueError):
                update.message.reply_text('Usage: /myaddress')
                logging.warning('[TRYERROR] /myaddress:{} invalid address' .format(
                    update.message.chat_id))
        else:
            update.message.reply_text(private_msg)
            logging.info('[RESPONSE] /myaddress:{} {}' .format(
                update.message.chat_id, private_msg))
    logging.info('[COMPLETE] /myaddress:{}' .format(update.message.chat_id))

def get_my_rank(update, context):
    """Get My Rank"""
    logging.info('[STARTING] /myrank:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False and update.message.chat_id > 0:
        logging.info('[DATABASE] /myrank:{} get address from database' .format(
            update.message.chat_id))
        connection = sqlite3.connect("bot.db")
        cursor = connection.cursor()
        row = cursor.execute(
            "SELECT address FROM users WHERE chat_id = ?",
            (update.message.chat_id,),
        ).fetchone()
        if row is None:
            update.message.reply_text(set_address_msg)
            logging.info('[DATABASE] /myrank:{} get address from database' .format(
                update.message.chat_id))
        else:
            my_address = row[0]
            logging.info('[DATABASE] /myrank:{} matched address {}' .format(
                update.message.chat_id, my_address))
            try:
                if is_address(my_address):
                    user_total = contract.functions.getPosition(my_address).call()
                    text = 'Rank: {}'
                    if user_total > 0:
                        update.message.reply_text(text .format(user_total))
                        logging.info('[RESPONSE] /myrank:{} user {} is ranked {}'
                                    .format(update.message.chat_id, my_address, user_total))
                    else:
                        update.message.reply_text("This address does not have a rank.")
                        logging.info('[RESPONSE] /myrank:{} user {} has no rank {}' .format(
                            update.message.chat_id, my_address, user_total))
                    connection.close()
                else:
                    update.message.reply_text('Address is invalid..')
                    logging.info('[RESPONSE] /myrank:{} address is invalid...'
                                .format(update.message.chat_id))
            except (IndexError, ValueError):
                update.message.reply_text('Usage: /myrank requires /setmyaddress')
                logging.warning('[TRYERROR] /myrank:{} requires /setmyaddress'
                            .format(update.message.chat_id))
    else:
        update.message.reply_text(private_msg)
        logging.info('[RESPONSE] /myrank:{} {}'.format(update.message.chat_id, private_msg))
    logging.info('[COMPLETE] /myrank:{}' .format(update.message.chat_id))

def get_my_rewards(update, context):
    """Get the user's rewards"""
    logging.info('[STARTING] /myrewards:{}'.format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        if update.message.chat_id > 0:
            logging.info('[DATABASE] /myrewards:{} get address from database' .format(
                update.message.chat_id))
            connection = sqlite3.connect("bot.db")
            cursor = connection.cursor()
            row = cursor.execute(
                "SELECT address FROM users WHERE chat_id = ?",
                (update.message.chat_id,),
            ).fetchone()
            if row is None:
                update.message.reply_text(set_address_msg)
                logging.info('[DATABASE] /myrewards:{} no match'.format(update.message.chat_id))
            else:
                my_address = row[0]
                logging.info('[DATABASE] /myrewards:{} matched address {}' .format(
                    update.message.chat_id, my_address))
                try:
                    if is_address(my_address):
                        logging.info('[LCWQUERY] /myrewards:{} {}' .format(
                            update.message.chat_id, lcw_url))
                        response = get_live_coin_watch(update, context)
                        var9 = response["rate"]
                        user_total = contract.functions.getGlqToClaim(my_address).call()
                        user_in_wei = web3.fromWei(user_total, 'ether')
                        eth_format = ("{:,.2f}".format(user_in_wei))
                        u_total = float(user_in_wei) * var9
                        f_total = ("{:,.2f}".format(u_total))
                        text = 'Unclaimed rewards: {} GLQ || Value ≈ ${}'
                        update.message.reply_text(text .format(eth_format, f_total))
                        logging.info('[RESPONSE] /myrewards:{} user rewards {} ≈ {}'
                                    .format(update.message.chat_id, eth_format, f_total))
                        connection.close()
                    else:
                        logging.warning('[RESPONSE] /myrewards:{} address is invalid...'
                                        .format(update.message.chat_id))
                        update.message.reply_text('Address is invalid..')
                except (IndexError, ValueError):
                    update.message.reply_text('There are no rewards at this address.')
                    logging.info('[TRYERROR] /myrewards:{} no rewards at this address'
                                .format(update.message.chat_id))
        else:
            update.message.reply_text(private_msg)
            logging.info('[RESPONSE] {}'.format(private_msg))
    logging.info('[COMPLETE] /myrewards:{}'.format(update.message.chat_id))

def get_my_tier(update, context):
    """Get users tier"""
    logging.info('[STARTING] /mytier:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        if update.message.chat_id > 0:
            logging.info('[DATABASE] /mytier:{} get address from database' .format(
                update.message.chat_id))
            connection = sqlite3.connect("bot.db")
            cursor = connection.cursor()
            row = cursor.execute(
                "SELECT address FROM users WHERE chat_id = ?",
                (update.message.chat_id,),
            ).fetchone()
            if row is None:
                logging.info('[DATABASE] /mytier:{} no match' .format(update.message.chat_id))
                update.message.reply_text('/setaddress must be set first.')
            else:
                my_address = row[0]
                logging.info('[DATABASE] /mytier:{} matched address {}'
                            .format(update.message.chat_id, my_address))
                try:
                    if is_address(my_address):
                        user_total = contract.functions.getWalletCurrentTier(my_address).call()
                        text = 'You are in tier: {}'
                        update.message.reply_text(text .format(user_total))
                        logging.info('[RESPONSE] /mytier:{} user in tier {}' .format(
                            update.message.chat_id, user_total))
                        connection.close()
                    else:
                        update.message.reply_text('Address is invalid...')
                        logging.info('[RESPONSE] /mytier:{} address is invalid...'
                                    .format(update.message.chat_id))
                except (IndexError, ValueError):
                    update.message.reply_text('This address has no tier.')
                    logging.warning('[TRYERROR] /mytier:{} address has no tier'.format(
                        update.message.chat_id))
        else:
            update.message.reply_text(private_msg)
            logging.info('[RESPONSE] /mytier:{} {}'.format(update.message.chat_id, private_msg))
    logging.info('[COMPLETE] /mytier:{}'.format(update.message.chat_id))

def get_my_total(update, context):
    """Total Staked"""
    logging.info('[STARTING] /mytotal:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        if update.message.chat_id > 0:
            logging.info('[DATABASE] /mytotal:{} get user address from database' .format(
                update.message.chat_id))
            connection = sqlite3.connect("bot.db")
            cursor = connection.cursor()
            row = cursor.execute(
                "SELECT address FROM users WHERE chat_id = ?",
                (update.message.chat_id,),
            ).fetchone()
            if row is None:
                logging.info('[DATABASE] /mytotal:{} address not set' .format(
                    update.message.chat_id))
                update.message.reply_text("You must first use /setaddress")
            else:
                address = row[0]
                try:
                    if is_address(address):
                        logging.info('[LCWQUERY] /mytotal:{} {}' .format(
                            update.message.chat_id, lcw_url))
                        response = get_live_coin_watch(update, context)
                        rate = response["rate"]
                        user_total = contract.functions.getDepositedGLQ(address).call()
                        user_in_wei = web3.fromWei(user_total, 'ether')
                        u_total = float(user_in_wei) * rate
                        f_total = ("{:,.2f}".format(u_total))
                        eth_format = ("{:,.2f}".format(user_in_wei))
                        #ethFormat = f"{userInWei:,}"
                        text = "You are staking: {} GLQ || Value ≈ ${}"
                        update.message.reply_text(text .format(eth_format, f_total))
                        logging.info("""[RESPONSE] /mytotal:{} user is staking: {} GLQ || Value ≈
                                    ${}""" .format(update.message.chat_id, eth_format, f_total))
                        connection.close()
                    else:
                        update.message.reply_text('Address is invalid...')
                        logging.info('[RESPONSE] /mytotal:{} Addess is invalid...'
                                    .format(update.message.chat_id))
                except (IndexError, ValueError):
                    update.message.reply_text('Usage: /total after you /set your address')
                    logging.warning('[TRYERROR] /mytotal:{} Usage: /total after /set'
                                .format(update.message.chat_id))
        else:
            update.message.reply_text(private_msg)
            logging.info('[RESPONSE] /mytotal:{} {}'.format(update.message.chat_id, private_msg))
    logging.info('[COMPLETE] /mytotal:{}' .format(update.message.chat_id))

########     MAIN GETTER FUNCTIONS    #########

def get_apy(update, context):
    """APYs"""
    logging.info('[STARTING] /apy:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        logging.info('[CONTRACT] /apy:{} getTiersAPY' .format(update.message.chat_id))
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
        logging.info('[RESPONSE] /apy:{} Tier 1: {}% Tier 2: {}% Tier 3: {}%'
                    .format(update.message.chat_id, tiers_apy[0], tiers_apy[1], tiers_apy[2]))
    logging.info('[COMPLETE] /apy:{}' .format(update.message.chat_id))

def get_tiers(update, context):
    """Get Tiers"""
    logging.info('[STARTING] /tiers:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        tier_totals = get_tier_totals()
        formatted_tiers = format_tiers(tier_totals)
        send_tiers_response(update, formatted_tiers)
        logging.info('[RESPONSE] /tiers:{}' .format(update.message.chat_id))
    logging.info('[COMPLETE] /tiers:{}' .format(update.message.chat_id))

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
    logging.info('[STARTING] /top:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        tops = contract.functions.getTopStakers().call()
        response = get_live_coin_watch(update, context)
        formatted_top_three = format_top_stakers(tops)
        formatted_values = format_staker_values(tops)
        send_top_stakers_response(update, formatted_top_three, formatted_values, response["rate"])
        logging.info('[RESPONSE] /top:{}' .format(update.message.chat_id))
    logging.info('[COMPLETE] /top:{}' .format(update.message.chat_id))

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
    logging.info('[STARTING] /totalstaked:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        logging.info('[LCWQUERY] /totalstaked:{} {}' .format(update.message.chat_id, lcw_url))
        try:
            response = get_live_coin_watch(update, context)
            rate = response["rate"]
            total_tier1 = contract.functions.getTierTotalStaked(1).call()
            total_tier2 = contract.functions.getTierTotalStaked(2).call()
            total_tier3 = contract.functions.getTierTotalStaked(3).call()
            tier1_in_wei = web3.fromWei(total_tier1, 'ether')
            tier2_in_wei = web3.fromWei(total_tier2, 'ether')
            tier3_in_wei = web3.fromWei(total_tier3, 'ether')
            staked_t = tier1_in_wei + tier2_in_wei + tier3_in_wei
            u_total = float(staked_t) * rate
            f_total = ("{:,.2f}".format(u_total))
            eth_format = ("{:,.2f}".format(staked_t))
            table = PrettyTable()
            table.field_names = ['Staked GLQ', 'Value']
            table.add_row([eth_format, '$' + f_total])
            response = '```\n{}```'.format(table.get_string())
            update.message.reply_text(response, parse_mode='Markdown')
            logging.info('[RESPONSE] /totalstaked:{} Staked GLQ: {} || Value ≈ ${}'
                        .format(update.message.chat_id, eth_format, f_total))
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /staked')
            logging.info('[RESPONSE] /totalstaked:{} usage /staked')
    logging.info('[COMPLETE] /totalstaked:{}' .format(update.message.chat_id))

def get_total_stakers(update, context):
    """Stakers"""
    logging.info('[STARTING] /totalstakers:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        logging.info('[CONTRACT] /totalstakers:{} getTotalStakers' .format(update.message.chat_id))
        try:
            user_total = contract.functions.getTotalStakers().call()
            table = PrettyTable()
            table.field_names = ['Total Stakers']
            table.add_row([user_total])
            response = '```\n{}```'.format(table.get_string())
            update.message.reply_text(response, parse_mode='Markdown')
            logging.info('[RESPONSE] /totalstakers:{} totalStakers:{}'
                        .format(update.message.chat_id, user_total))
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /stakers')
            logging.info('[RESPONSE] /totalstakers:{} usage: /stakers' .format(
                update.message.chat_id))
    logging.info('[COMPLETE] /totalstakers:{}' .format(update.message.chat_id))

#########     LIST INFO FUNCTIONS    ##########

def get_websites(update, context):
    """Websites"""
    logging.info('[STARTING] /websites:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        try:
            table = PrettyTable()
            table.align = "l"
            table.field_names = ["Name", "URL"]
            for website in websites:
                table.add_row(website)
            response = '```\n{}```'.format(table.get_string())
            update.message.reply_text(response, parse_mode='Markdown')
            logging.info('[RESPONSE] /websites:{} sent websites' .format(update.message.chat_id))
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /websites')
            logging.info('[RESPONSE] /websites:{} usage: /websites' .format(
                update.message.chat_id))
    logging.info('[COMPLETE] /websites:{}' .format(update.message.chat_id))

def get_socials(update, context):
    """Socials"""
    logging.info('[STARTING] /socials:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        try:
            table = PrettyTable()
            table.align = "l"
            table.field_names = ["Name", "URL"]
            for social in socials:
                table.add_row(social)
            response = '```\n{}```'.format(table.get_string())
            update.message.reply_text(response, parse_mode='Markdown')
            logging.info('[RESPONSE] /socials:{} sent socials' .format(update.message.chat_id))
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /socials')
            logging.info('[RESPONSE] /socials:{} usage: /socials' .format(update.message.chat_id))
    logging.info('[COMPLETE] /socials:{}' .format(update.message.chat_id))

def get_staking(update, context):
    """Staking Info"""
    logging.info('[STARTING] /staking:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        try:
            table = PrettyTable()
            table.align = "l"
            table.field_names = ["Name", "URL"]
            for stake in staking:
                table.add_row(stake)
            response = '```\n{}```'.format(table.get_string())
            update.message.reply_text(response, parse_mode='Markdown')
            logging.info('[RESPONSE] /staking:{} sent staking' .format(update.message.chat_id))
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /staking')
            logging.info('[RESPONSE] /staking:{} usage: /staking' .format(update.message.chat_id))
    logging.info('[COMPLETE] /staking:{}' .format(update.message.chat_id))

def get_documentation(update, context):
    """Documentation Info"""
    logging.info('[STARTING] /documentation:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        try:
            table = PrettyTable()
            table.field_names = ['Site', 'Link']
            table.add_row(['Docs', 'https://glq.link/docs'])
            response = '```\n{}```'.format(table.get_string())
            update.message.reply_text(response, parse_mode='Markdown')
            logging.info('[RESPONSE] /documentation:{} sent documentation' .format(
                update.message.chat_id))
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /documentation')
            logging.info('[RESPONSE] /documentation:{} usage: /documentation' .format(
                update.message.chat_id))
    logging.info('[COMPLETE] /documentation:{}' .format(update.message.chat_id))

def get_short_cuts(update, context):
    """Shortcuts Info"""
    logging.info('[STARTING] /shortcuts:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        try:
            table = PrettyTable()
            table.align = "l"
            table.field_names = ["Command", "Shortcut"]
            for shortcut in shortcuts:
                table.add_row(shortcut)
            response = '```\n{}```'.format(table.get_string())
            update.message.reply_text(response, parse_mode='Markdown')
            logging.info('[RESPONSE] /shortcuts:{} sent shortcuts' .format(update.message.chat_id))
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /socials')
            logging.info('[RESPONSE] /shortcuts:{} usage: /shortcuts' .format(
                update.message.chat_id))
    logging.info('[COMPLETE] /shortcuts:{}' .format(update.message.chat_id))

def get_listings(update, context):
    """CEX/DEX Listings"""
    logging.info('[STARTING] /listings:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        try:
            table = PrettyTable()
            table.align = "l"
            table.field_names = ["Name", "Pair", "URL"]
            for cex_listing in cex_listings:
                table.add_row(cex_listing)
            for dex_listing in dex_listings:
                table.add_row(dex_listing)
            response = '```\n{}```'.format(table.get_string())
            update.message.reply_text(response, parse_mode='Markdown')
            logging.info('[RESPONSE] /listings:{} sent listings' .format(update.message.chat_id))
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /listings')
            logging.info('[RESPONSE] /listings:{} usage: /listings' .format(
                update.message.chat_id))
    logging.info('[COMPLETE] /listings:{}' .format(update.message.chat_id))

def get_status(update, context):
    """Monitor Status"""
    logging.info('[STARTING] /status:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        try:
            table = PrettyTable()
            table.align = "l"
            table.field_names = ["Name", "URL"]
            for stat in status:
                table.add_row(stat)
            response = '```\n{}```'.format(table.get_string())
            update.message.reply_text(response, parse_mode='Markdown')
            logging.info('[RESPONSE] /status:{} sent status' .format(update.message.chat_id))
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /status')
            logging.info('[RESPONSE] /status:{} usage: /status' .format(update.message.chat_id))
    logging.info('[COMPLETE] /status:{}' .format(update.message.chat_id))

def get_apply(update, context):
    """Developer Application"""
    logging.info('[STARTING] /apply:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        logging.info('[RESPONSE] /apply:{}' .format(update.message.chat_id))
        update.message.reply_text(apply)
    logging.info('[COMPLETE] /apply:{}' .format(update.message.chat_id))

#######     LIVECOINWATCH  FUNCTIONS    #######

def get_live_coin_watch(update, context):
    """LiveCoinWatch Fetch"""
    logging.info('[STARTING] /lcwquery:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        logging.info('[LCWQUERY] /lcwquery:{} {}' .format(update.message.chat_id, lcw_url))
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
        #response = "Price: ${}\nVolume: ${}\nATH: ${}\nMcap: ${}"
        logging.info('[RESPONSE] /lcwquery:{} Price: {}'
                    .format(update.message.chat_id, rate))
        logging.info('[COMPLETE] /lcwquery:{}' .format(update.message.chat_id))
    return resp_json

def live_coin_watch_fiats(update, context):
    """LiveCoinWatch Fiats"""
    logging.info('[STARTING] /lcwfiats:{}' .format(update.message.chat_id))
    if get_maint_mode(update, context) is False:
        logging.info('[LCWQUERY] /lcwfiats:{} {}' .format(update.message.chat_id, lcw_fiats_url))
        payload = '{}'
        headers = {
            'content-type': 'application/json',
            'x-api-key': lcw_api_key
        }
        resp_post = requests.request("POST", lcw_fiats_url, headers=headers, data=payload)
        resp_json = json.loads(resp_post.text)
        response = "Data Fetched"
        logging.info('[RESPONSE] /lcwfiats:{} {}' .format(update.message.chat_id, response))
        logging.info('[COMPLETE] /lcfiats:{}' .format(update.message.chat_id))
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

########     MAINTENANCE  FUNCTIONS    ########

def get_maint_mode(update, context):
    """Check if maintenance mode is enabled."""
    if context is None:
        logging.warning('[USERMODE] No context available')
    if maint_mode == 1:
        if update.message.chat_id == allowed_admin:
            logging.info('[USERMODE] Maintenance: ON | Admin Allowed')
            return False
        logging.warning('[USERMODE] Maintenance: ON | Not Admin')
        update.message.reply_text(maint_mode_msg)
        return True
    logging.info('[USERMODE] Maintenance: OFF | Not Admin')
    return False

def log_maint_mode():
    """Runs at first start to log maintenance mode."""
    if maint_mode == 1:
        logging.warning('[USERMODE] {}' .format(maint_mode_log_msg_on))
        logging.warning('[USERMODE] Admin: {}'.format(allowed_admin))
    else:
        logging.info('[USERMODE] {}' .format(maint_mode_log_msg_off))

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


def main():
    """Main"""
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
    # Start Polling
    logging.info('[USERMODE] Starting Scheduler')
    updater.start_polling()
    updater.idle()

# Initialize
if __name__ == '__main__':
    main()
