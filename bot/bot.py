# -*- coding: utf-8 -*-
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
from telegram.ext import Updater, CommandHandler, ConversationHandler
import logging
from database.users import get_user_wrapper, add_new_user, user_registered, init
from .trackables import *
from .reporting import report_conversation
from .reminder import enable_reminders_command

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

stat_img_filename = '/Users/oleg/PycharmProjects/LifeStatsBot/fig.png'
str_add_new = 'add new thing you want to track'
str_report = 'report today\'s performance'
str_stat = 'see statistics'

def _start(bot, update):
    update.message.reply_text(
        "Hi! This bot helps you track and measure your life. "
        "telegram To get started, send /add_trackable. If you want to get ideas "
        "what you can use this bot for, send /help."
        # , reply_markup=markup
    )

    user_id = update.message.chat.id

    if not user_registered(user_id):
        print("user doesnt exist!!")
        add_new_user(user_id, update.message.chat.username)
    else:
        print('user exists')

def done(bot, update, user_data):
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text("I learned these facts about you: ajajajajajaja")

    user_data.clear()
    return ConversationHandler.END

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def start():
    init()
# Set these variable to the appropriate values
    TOKEN = "565922953:AAHLDSH9RcfKD2i9swjrgAL8_joW0ashCkU"
    NAME = "vast-citadel-21137"

    # Port is given by Heroku
    PORT = os.environ.get('PORT')

    # Create the Updater and pass it your bot's token.
    # updater = Updater("552042340:AAHtT3JtHDySdLFr59-jkRNZUP_LSOB-WDE")
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', _start))

    dp.add_handler(CommandHandler('trackables', print_all_trackables))
    dp.add_handler(add_trackable_conv())
    dp.add_handler(delete_trackable_command())
    
    dp.add_handler(report_conversation())

    dp.add_handler(enable_reminders_command())

    # log all errors
    dp.add_error_handler(error)

    # # Start the Bot
    updater.start_polling()

    # # Start the webhook
    # updater.start_webhook(listen="0.0.0.0",
    #                       port=int(PORT),
    #                       url_path=TOKEN)
    # updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
    updater.idle()

