'''
    module for adding new trackables, listing existing,
    and adding new user entries to them 
'''
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, StringCommandHandler
from telegram.ext.filters import Filters
from database.users import get_user_wrapper
from .utils import get_user, fallback_cb
import re

AWAITING_PROP_NAME, AWAITING_LOWER_BOUND, AWAITING_UPPER_BOUND = range(3)

def add_trackable_conv():
    return ConversationHandler(
        entry_points=[CommandHandler('add_trackable', _add_trackable, pass_user_data=True)],
        states={
            AWAITING_PROP_NAME: [
                MessageHandler(Filters.text,
                             _recieved_propname,
                             pass_user_data=True),
            ],
            AWAITING_LOWER_BOUND: [
                MessageHandler(Filters.text,
                             _recieved_lower_bound,
                             pass_user_data=True),
            ],
            AWAITING_UPPER_BOUND: [
                MessageHandler(Filters.text,
                             _recieved_upper_bound,
                             pass_user_data=True),
            ],
        },

        fallbacks=[MessageHandler(Filters.text, fallback_cb, pass_user_data=True)]
    )

def delete_trackable_command():
    return CommandHandler('remove_trackable', _delete_trackable, pass_args=True)

def _delete_trackable(bot, update, args):
    print(args[0])

    user = get_user(update)
    trackname = args[0]

    if user.trackable_registered(trackname):
        user.delete_trackable(trackname)
        update.message.reply_text('all your history of handling {0} is deleted'.format(trackname))
    else:
        update.message.reply_text('But you don\'t track the {0}'.format(trackname))

def print_all_trackables(bot, update):
    print("printing all trackables")

    user = get_user(update)

    reply_msg = '\n'.join(user.trackable_names) if user.trackable_names \
        else 'You don\'t have anything to track yet. Add something via the /add_trackable command'
    
    update.message.reply_text(reply_msg)

#region add trackable
def _add_trackable(bot, update, user_data):
    update.message.reply_text("Ok. What it is you want to measure?")
    return AWAITING_PROP_NAME

def _recieved_propname(bot, update, user_data):

    user_data['prop_name'] = update.message.text
    update.message.reply_text(
        "Got it. You will measure in some units. What is the lowest value of that unit? For example, 1")
    return AWAITING_LOWER_BOUND

def _recieved_lower_bound(bot, update, user_data):
    entered_val = update.message.text
    
    if not _is_pos_digit(entered_val):
        update.message.reply_text('Only positive digits are allowed. Try again')
        return AWAITING_LOWER_BOUND


    user_data['lower_bound'] = entered_val
    update.message.reply_text("And what is the highest value? Write 0 for unbound values.")
    return AWAITING_UPPER_BOUND

def _recieved_upper_bound(bot, update, user_data):

    entered_val = update.message.text

    if not _is_pos_digit(entered_val):
        update.message.reply_text('Only positive digits are allowed. Try again')
        return AWAITING_UPPER_BOUND

    user_data['upper_bound'] = entered_val

    print(user_data)
    update.message.reply_text(
        "Great! You just started tracking {0}. At the evening, I'll ask you how good you did today."
        " Then after a while, you can see the statistics of {1}!"
        .format(user_data['prop_name'], user_data['prop_name']))

    user = get_user(update)
    user.register_trackable(user_data['prop_name'])

    #TODO: save bounds

    return ConversationHandler.END


int_re = re.compile('\\d+')
def _is_pos_digit(str):
    return int_re.match(str) is not None
#endregion
