'''
    module for adding new trackables, listing existing,
    and adding new user entries to them 
'''

from telegram.ext import ConversationHandler, CommandHandler, RegexHandler
from database.users import get_user_wrapper
from .utils import get_user

ADD_PROP_NAME, ADD_LOWER_BOUND, ADD_UPPER_BOUND = range(3)

def add_trackable_conv():
    return ConversationHandler(
        entry_points=[CommandHandler('add_trackable', _add_trackable, pass_user_data=True)],
        states={
            ADD_PROP_NAME: [
                RegexHandler('.+',
                             _add_lower_bound,
                             pass_user_data=True),
            ],
            ADD_LOWER_BOUND: [
                RegexHandler('\\d+',
                             _add_upper_bound,
                             pass_user_data=True),
            ],
            ADD_UPPER_BOUND: [
                RegexHandler('\\d+',
                             _prop_added,
                             pass_user_data=True),
            ],
        },

        fallbacks=[RegexHandler('^Done$', _done, pass_user_data=True)]
    )

def delete_trackable_command():
    return CommandHandler('remove_trackable', _delete_trackable, pass_args=True)

def _delete_trackable(bot, update, args):
    print(args[0])
    get_user(update).delete_trackable(args[0])


def print_all_trackables(bot, update):
    print("printing all trackables")

    user = get_user(update)
    update.message.reply_text('\n'.join(user.trackable_names))

#region add trackable
def _done():
    print('\ndone called')

def _add_trackable(bot, update, user_data):
    update.message.reply_text("Ok. What it is you want to measure?"
                              " Write anything you want, you can change that later")
    return ADD_PROP_NAME

def _add_lower_bound(bot, update, user_data):
    user_data['prop_name'] = update.message.text
    update.message.reply_text(
        "Got it. You will measure in some units. What is the lowest value of that unit? For example, 1")
    return ADD_LOWER_BOUND

def _add_upper_bound(bot, update, user_data):
    user_data['lower_bound'] = update.message.text
    update.message.reply_text("And what is the highest value? Write 0 for unbound values.")
    return ADD_UPPER_BOUND

def _prop_added(bot, update, user_data):
    user_data['upper_bound'] = update.message.text
    print(user_data)
    update.message.reply_text(
        "Great! You just started tracking {}. At the evening, I'll ask you how good you did today."
        " Then after a while, you can see statistics of {}!"
        .format(user_data['prop_name'], user_data['prop_name']))

    user = get_user(update)
    user.register_trackable(user_data['prop_name'])

    return ConversationHandler.END
#endregion
