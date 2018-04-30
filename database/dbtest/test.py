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

def put_sample_data(user_id, trackable):

    start_date = datetime.utcnow() - timedelta(days=7)

    vals = [35, 25, 28, 33, 42, 44, 46]

    for i in range(8):
        
        get_use

        start_date += timedelta(days=1)



