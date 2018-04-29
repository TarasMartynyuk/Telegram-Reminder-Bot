
from database.users import get_user_wrapper
from datetime import datetime, timedelta

def get_user(update):
    return get_user_wrapper(update.message.chat.id)

def fallback_cb(bot, update, user_data):
    update.message.reply_text('Wow wait, i\'ve got confused (we have an error handling this particular branch of conversation, sorry)')
    user_data.clear()

def next_day(datetime):
    return

