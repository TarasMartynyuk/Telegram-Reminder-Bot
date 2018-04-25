from database.users import _get_users_col, add_new_user, get_user_wrapper
from inspect import stack
from database.utils import coll
from database.trackable import _trackable_coll_name


test_username = 'Taras'
test_track_name = 'jogging'

def set_up():
    _get_users_col().remove({})
    test_track_coll().remove({})

    new_us_wrapper = add_new_user(test_username)
    new_us_wrapper.register_trackable(test_track_name)

def track_test_instance():
    return get_user_wrapper(test_username).get_trackable_wrapper(test_track_name)



def log_passed():
    print('passed test: {0}'.format(stack()[1][3])) 

 
def test_track_coll():
    return  coll(_trackable_coll_name(test_username, test_track_name))