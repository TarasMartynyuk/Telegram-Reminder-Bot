from database.utils import DatabaseConsts as dc
from datetime import datetime
from inspect import stack
from database.trackable import TrackableDbWrapper, _trackable_coll, _trackable_coll_name
from database.users import _get_users_col, add_new_user, get_user_wrapper
from .dbprint import print_collection

test_username = 'Taras'
test_track_name = 'jogging'

def run_all_trackable_tests():
    StartDate_ReturnsNone_IfNotSet()
    StartDate_CreatesMetadataDoc_IfNotPresent()
    StartDate_PutValue_EqOrig()
    PutStartDate_Updates_PresentDoc()
    # _set_up()
    # print_collection(_get_users_col())
    # print_collection(_trackable_coll(test_track_name))


#region start_data
def StartDate_ReturnsNone_IfNotSet():
    _set_up()
    tr = _track_test_instance()

    assert tr.get_start_date() is None
    _log_passed()

def StartDate_PutValue_EqOrig():
    _set_up()
    tr = _track_test_instance()

    orig = datetime.utcnow()
    tr.set_start_date(orig)

    assert orig == tr.get_start_date()
    _log_passed()

def StartDate_CreatesMetadataDoc_IfNotPresent():
    _set_up()
    tr = _track_test_instance()

    orig = datetime.utcnow()
    tr.set_start_date(orig)

    assert tr.get_start_date() != None
    _log_passed()

def PutStartDate_Updates_PresentDoc():
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
    _log_passed()
#endregion

#region bounds

def GetBounds_ReturnsNone_IfNotSet():
    _set_up()
    tr = _track_test_instance()

    assert tr.get_bounds is None

def  get_bounds_creates_new_metadoc_if_not_present():
    _set_up()
    tr = _track_test_instance()

    orig = {
        'min' : 1,
        'max' : 10
    }

    tr.set_bounds(orig)

    assert tr.get_bounds() is not None




#endregion


def _print_trackable(tr):
    print_collection(_trackable_coll(tr.coll_name))

def _set_up():
    _get_users_col().remove({})
    _trackable_coll(_trackable_coll_name(test_username, test_track_name)).remove({})

    new_us_wrapper = add_new_user(test_username)
    new_us_wrapper.register_trackable(test_track_name)

def _track_test_instance():
    return get_user_wrapper(test_username).get_trackable_wrapper(test_track_name)


def _log_passed():
    print('passed test: {0}'.format(stack()[1][3]))  
