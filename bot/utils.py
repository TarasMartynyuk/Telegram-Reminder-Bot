
from database.users import get_user_wrapper

def get_user(update):
    return get_user_wrapper(update.message.chat.id)

