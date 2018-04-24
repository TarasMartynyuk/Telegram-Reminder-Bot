import database.users as us
from database.trackable import TrackableDbWrapper, _trackable_coll
from database.users import _get_users_col
from database.utils import DatabaseConsts as dc
from .dbprint import print_all_users, print_collection
from .trackable_test import run_all_trackable_tests

def test():
    # time_test()
    # users_test()
    # trackable_test()
    run_all_trackable_tests()
    pass

def users_test():
    _get_users_col().remove({})
    new_us_wrapper = us.add_new_user('Taras')

    # print_all_users()

    # print("{0}\n".format(new_us_wrapper))


    print("\n")
    
    # print_all_users()




def time_test():
    from time import time
    from datetime import datetime

    print(datetime.utcnow().timestamp())
    print(time())

    
    pass





