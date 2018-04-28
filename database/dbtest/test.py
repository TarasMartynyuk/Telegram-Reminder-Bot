from .trackable_test import run_all_trackable_tests
from database.users import _get_users_col
from database.utils import DatabaseConsts as dc

def test_all():
    run_all_trackable_tests()
    pass

def drop_users():
    _get_users_col().drop()

def drop_db():
    dc.CLIENT.drop_database(dc.DATABASE_NAME)

def drop_trackable_entries():
    pass

