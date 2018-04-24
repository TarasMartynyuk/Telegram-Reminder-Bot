from .dbprint import print_all_users
import database.users as us
from database.utils import get_users_col

def test():
    users_test()

def users_test():
    us.init()
    # get_users_col().remove({})
    # us.add_new_user('Taras')
    # us.get_user('Taras')

    print_all_users()







