from .trackable_test import run_all_trackable_tests
from database.users import _get_users_col

def test_all():
    run_all_trackable_tests()
    pass

def drop_users():
    _get_users_col().drop()

def drop_user_trackables(user, trackable):
    pass

def drop_trackable_entry():
    pass

