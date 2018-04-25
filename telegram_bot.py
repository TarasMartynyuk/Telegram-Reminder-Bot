#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import os
from datetime import datetime
from datetime import timedelta
from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)


# import matplotlib.pyplot as plt
# import matplotlib


import logging
import re

from database.users import *
from database.trackable import *
init()


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, PROP_ADDED, ADD_PROP_NAME, ADD_LOWER_BOUND, ADD_UPPER_BOUND, \
SHOW_STATS, START_REPORTING, ASK_FOR_TRACKABLE_REPORT, GET_TRACKABLE_REPORT = range(9)

stat_img_filename = '/Users/oleg/PycharmProjects/LifeStatsBot/fig.png'
str_add_new = 'add new thing you want to track'
str_report = 'report today\'s performance'
str_stat = 'see statistics'


# options_keyboard = [
#     [str_add_new],
#     [str_report],
#     [str_stat]
# ]
#
# markup = ReplyKeyboardMarkup(options_keyboard, one_time_keyboard=True)


# region stubs

def user_exists(user_name):
    return user_registered(user_name)


# def add_new_user(user_name):
#     logger.info("trying to add new user");
#     return


# def add_trackable(user_name, trackable):
#     logger.info("added %s for %s", trackable, user_name)
#     return


def add_new_user_entry(user_name, trackable, val):
    logger.info("adding entry for %s : %s", trackable, str(val))
    return


# def get_all_trackables(user_name):
#     logger.info("getting all trackables")
#     return ["learning", "reading"]


# def get_trackable_metadata(user_name, trackable):
#     return {
#         "learning": {
#             "lower_bound": 1,
#             "upper_bound": 10,
#             "start_date": datetime.date(2010, 5, 24)
#         },
#         "reading": {
#             "lower_bound": 0,
#             "upper_bound": 0,
#             "start_date": datetime.date(2010, 5, 22)
#         }
#     }[trackable]


def get_n_last_entries(user_name, trackable, n):
    return {
        "learning": [
            {
                "date": datetime(2018, 4, 17),
                "val": 1
            },
            {
                "date": datetime(2018, 4, 18),
                "val": 2
            },
            {
                "date": datetime(2018, 4, 19),
                "val": 3
            },
            {
                "date": datetime(2018, 4, 20),
                "val": 2
            },
            {
                "date": datetime(2018, 4, 21),
                "val": 5
            },
            {
                "date": datetime(2018, 4, 22),
                "val": 7
            },
            {
                "date": datetime(2018, 4, 23),
                "val": 3
            }
        ]
    }[trackable]



def delete_trackable_by_name(user_name, trackable):
    return

# endregion


def user_id_from_update(update):
    return update.message.chat.id


def start(bot, update):
    update.message.reply_text(
        "Hi! This bot helps you track and measure your life. "
        "telegram To get started, send /add_trackable. If you want to get ideas "
        "what you can use this bot for, send /help."
        # , reply_markup=markup
    )

    user_id = user_id_from_update(update)
    if not user_exists(user_id):
        add_new_user(user_id)

    return CHOOSING


# region add_new
def add_new(bot, update, user_data):
    update.message.reply_text("Ok. What it is you want to measure?"
                              " Write anything you want, you can change that later")
    return ADD_PROP_NAME


def add_lower_bound(bot, update, user_data):
    user_data['prop_name'] = update.message.text
    update.message.reply_text(
        "Got it. You will measure in some units. What is the lowest value of that unit? For example, 1")
    return ADD_LOWER_BOUND


def add_upper_bound(bot, update, user_data):
    user_data['lower_bound'] = update.message.text
    update.message.reply_text("And what is the highest value? Write 0 for unbound values.")
    return ADD_UPPER_BOUND


def prop_added(bot, update, user_data):
    user_data['upper_bound'] = update.message.text
    print(user_data)
    update.message.reply_text(
        "Great! You just started tracking {}. At the evening, I'll ask you how good you did today."
        " Then after a while, you can see statistics of {}!"
        .format(user_data['prop_name'], user_data['prop_name']))

    # add_trackable(user_id_from_update(update), user_data['prop_name'])
    user = get_user_wrapper(user_id_from_update(update))
    user.register_trackable(user_data['prop_name'])
    trackable = user.get_trackable_wrapper(user_data['prop_name'])
    trackable.set_start_date(datetime.now())
    trackable.set_bounds({
        "min": user_data['lower_bound'],
        "max": user_data['upper_bound']
    })
    # TODO: anything else?

    return ConversationHandler.END


# endregion

# region show stats

def trackable_and_date_tokens(tokens):
    if len(tokens) >= 2:
        if len(tokens) >= 4:
            mb_number_of, mb_time_units = tokens[-2:]
            if re.match(r"^[1-9]\d*$", mb_number_of) and re.match("^(week|month|day|year)$", mb_time_units):
                # last two tokens are number_of time_units, so
                return tokens[1:-2], tokens[-2:]
            else:
                return tokens[1:], ['1', 'week']
        else:
            return tokens[1:], ['1', 'week']
    else:
        return None, None


def date_back(number_of, time_unit):
    if time_unit == 'week':
        return datetime.now() - timedelta(weeks=int(number_of)), number_of * 7
    if time_unit == 'day':
        return datetime.now() - timedelta(days=int(number_of)), number_of
    if time_unit == 'month':
        return datetime.now() - timedelta(months=int(number_of)), number_of * 30
    if time_unit == 'year':
        return datetime.now() - timedelta(years=int(number_of)), number_of * 365
    raise KeyError('{} is not day, week, etc.'.format(time_unit))

def show_stats(bot, update, user_data, req):
    update.message.reply_text("Stats: from {} to {}".format(req['from'], req['to']))
    print(get_n_last_entries(user_id_from_update(update), req['trackable'], req['entry_n']))
    # save_stats_img([entry['val'] for entry in get_n_last_entries(user_id_from_update(update), req['trackable'], req['entry_n'])])
    # bot.send_photo(chat_id=update.message.chat.id, photo=open(stat_img_filename, 'rb'))
    # TODO: install matplotlib or sth


def show_stats_request(bot, update, user_data):
    '''
    usage: /stats trackable_name number_of time_units
    '''
    # write what statistics he wants to see
    # ask time range
    # or show it for one week and ask if he wants to change the range
    # or maybe let statistics be a command
    # /stats learning 1 week
    # /stats learning 1 month
    # /stats learning 1 day
    # /stats learning 1 year
    # this means he must type trackable name
    # /trackables lists all trackables he has
    # /add_trackable start conversation about his new trackable
    # /report
    # /help write some basic tutorial-like stuff

    user = get_user_wrapper(user_id_from_update(update))
    tokens = update.message.text.split()
    if len(tokens) == 1:
        # no args, ignore or sth
        update.message.reply_text("usage: /stats trackable_name number_of time_units")
    else:
        mb_trackable_tokens, date_tokens = trackable_and_date_tokens(tokens)
        mb_trackable = ' '.join(mb_trackable_tokens)
        if mb_trackable in user.trackable_name:
            start_date, days_num = date_back(date_tokens[0], date_tokens[1])
            stats_request = {
                "trackable": mb_trackable,
                "from": start_date,
                "to": datetime.now(),
                "entry_n": days_num
            }
            show_stats(bot, update, user_data, stats_request)
        else:
            update.message.reply_text("there is no trackable {}".format(mb_trackable))


def save_stats_img(nums):
    matplotlib.style.use('seaborn')
    plt.plot(range(len(nums)), nums)
    plt.gcf().savefig(stat_img_filename)


# endregion

#region report update sss

def start_reporting(bot, update, user_data):
    user = get_user_wrapper(user_id_from_update(update))
    # user_data['trackables'] = get_all_trackables(user_id_from_update(update))
    user_data['trackables'] = user.trackable_names;
    if len(user_data['trackables']) > 0:
        update.message.reply_text("Oh, wonderful!")
        user_data['index_of_curr_trackable'] = 0
        user_data['report_data'] = {}
        return ask_for_trackable_report(bot, update, user_data)
    else:
        update.message.reply_text("You don't have any trackables yet. Create one by sending /add_trackable")
        return CHOOSING


def ask_for_trackable_report(bot, update, user_data):
    if user_data['index_of_curr_trackable'] != len(user_data['trackables']):
        trackable = user_data['trackable'] = user_data['trackables'][user_data['index_of_curr_trackable']]
        user_data['index_of_curr_trackable'] += 1
        update.message.reply_text("How is {} going?".format(trackable))
        return GET_TRACKABLE_REPORT
    else:
        for trackable, val in user_data['report_data'].iteritems():
            add_new_user_entry(user_id_from_update(update), trackable, val)
        update.message.reply_text("Thank your for your participation!")
        return ConversationHandler.END


def get_trackable_report(bot, update, user_data):
    trackable = user_data['trackable']
    user_data['report_data'][trackable] = int(update.message.text)
    return ask_for_trackable_report(bot, update, user_data)


#endregion


def trackables_command(bot, update):
    update.message.reply_text('\n'.join(get_user_wrapper(user_id_from_update(update)).trackable_names))

def done(bot, update, user_data):
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text("I learned these facts about you: ajajajajajaja")

    user_data.clear()
    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
# Set these variable to the appropriate values
    TOKEN = "565922953:AAHLDSH9RcfKD2i9swjrgAL8_joW0ashCkU"
    NAME = "vast-citadel-21137"

    # Port is given by Heroku
    PORT = os.environ.get('PORT')

    # Create the Updater and pass it your bot's token.
    # updater = Updater("552042340:AAHtT3JtHDySdLFr59-jkRNZUP_LSOB-WDE")
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    add_trackable_conversation = ConversationHandler(
        entry_points=[CommandHandler('add_trackable', add_new, pass_user_data=True)],
        states={
            ADD_PROP_NAME: [
                RegexHandler('.+',
                             add_lower_bound,
                             pass_user_data=True),
            ],
            ADD_LOWER_BOUND: [
                RegexHandler('\\d+',
                             add_upper_bound,
                             pass_user_data=True),
            ],
            ADD_UPPER_BOUND: [
                RegexHandler('\\d+',
                             prop_added,
                             pass_user_data=True),
            ],
        },

        fallbacks=[RegexHandler('^Done$', done, pass_user_data=True)]
    )

    start_reporting_conversation = ConversationHandler(
        entry_points=[CommandHandler('report', start_reporting, pass_user_data=True)],
        states={
            GET_TRACKABLE_REPORT: [
                RegexHandler('\\d+',
                             get_trackable_report,
                             pass_user_data=True)
            ]
        },
        fallbacks=[RegexHandler('^Done$', done, pass_user_data=True)]
    )

    show_stats_conversation = ConversationHandler(
        entry_points=[CommandHandler('stats', show_stats_request, pass_user_data=True)],
        states={

        },
        fallbacks=[RegexHandler('^Done$', done, pass_user_data=True)]
    )

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(start_reporting_conversation)
    dp.add_handler(add_trackable_conversation)
    dp.add_handler(CommandHandler('trackables', trackables_command))
    # dp.add_handler(show_stats_conversation)
    dp.add_handler(CommandHandler('stats', show_stats_request, pass_user_data=True))

    # log all errors
    dp.add_error_handler(error)

    # # Start the Bot
    # updater.start_polling()

    # Start the webhook
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
    

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
