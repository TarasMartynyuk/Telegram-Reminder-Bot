from .trackable_test import run_all_trackable_tests
from database.users import _get_users_col
from database.utils import DatabaseConsts as dc
from database.trackable import drop_trackable_collection
from datetime import datetime, timedelta, date
from database.users import get_user_wrapper
from .dbprint import _print_collection


def test_all():
    run_all_trackable_tests()
    pass

def drop_users():
    _get_users_col().drop()

def drop_db():
    dc.CLIENT.drop_database(dc.DATABASE_NAME)


def pretend_to_remind(bot, chat_id):
    '''
    sends a reminder to a user whose chat_id hardcoded value below
    '''
    demo_user_id = chat_id

    bot.send_message(chat_id=demo_user_id, text='Hey! It\'s time to tell me how you did today')
    pass


def put_sample_data(user_id, trackable):
    '''
    creates new trackable for user, 
    fills it with sample data for last week

    any prev data for this trackable is removed 
    '''

    user = get_user_wrapper(user_id)
    
    drop_trackable_collection(user.name, trackable)

    curr_date = datetime.utcnow() - timedelta(days=7)

    vals = [35, 25, 28, 33, 42, 44, 46]
    
    if not user.trackable_registered(trackable):
        user.register_trackable(trackable)
    
    tr = user.get_trackable_wrapper(trackable)

    from database.utils import DatabaseConsts as dc
    from database.utils import coll


    for i in range(7):
        tr.add_user_entry(curr_date, vals[i])

        curr_date += timedelta(days=1)


    



