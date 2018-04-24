from .dbprint import print_all_users
import database.users as us
import database.trackable as tr
from database.users import _get_users_col
from database.utils import DatabaseConsts as dc

def test():

    users_test()
    pass
    # trackable_test()

def users_test():
    _get_users_col().remove({})
    new_us_wrapper = us.add_new_user('Taras')

    print_all_users()

    # print("{0}\n".format(new_us_wrapper))

    new_us_wrapper.register_trackable('jogging')
    print("\n")

    print_all_users()


def trackable_test():
    pass





