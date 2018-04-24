from database.utils import DatabaseConsts as dc
from datetime import datetime
from database.trackable import TrackableDbWrapper, _trackable_coll
from database.users import _get_users_col, add_new_user, get_user_wrapper
from .dbprint import print_collection

test_username = 'Taras'
test_track_name = 'jogging'

def run_all_trackable_tests():
    put_start_date_creates_doc_if_not_present()
    put_start_date_updates_present_doc()


def put_start_date_creates_doc_if_not_present():
    _set_up()
    tr = _track_test_instance()

    orig = datetime.utcnow()

    tr.set_start_date(orig)
    retrieved = tr.get_start_date()

    d = datetime.utcnow()

    assert orig == retrieved


def put_start_date_updates_present_doc():
    _set_up()
    tr = _track_test_instance()
    assert datetime.utcnow() == datetime.utcnow()

    first = datetime.utcnow()
    tr.set_start_date(first)

    second = datetime.fromtimestamp(
        datetime.utcnow().timestamp() + 100000
    )
    
    tr.set_start_date(second)

    assert tr.get_start_date() == second







def _print_trackable(tr):
    print_collection(_trackable_coll(tr.coll_name))

def _set_up():
    _get_users_col().remove({})
    new_us_wrapper = add_new_user(test_username)
    new_us_wrapper.register_trackable(test_track_name)

def _track_test_instance():
    return get_user_wrapper(test_username).get_trackable_wrapper(test_track_name)



