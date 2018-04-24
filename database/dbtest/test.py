from .dbprint import print_all_users
import database.users as us
import database.trackable as tr
from database.utils import get_users_col

def test():
    users_test()
    # trackable_test()

def users_test():
    get_users_col().remove({})
    us_wrapper = us.add_new_user('Taras')
    print(us_wrapper.get_trackables())

    print_all_users()


def trackable_test():
    pass





