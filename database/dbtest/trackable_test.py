from database.utils import DatabaseConsts as dc
from datetime import datetime
from inspect import stack
from database.trackable import TrackableDbWrapper, _trackable_coll_name
from database.users import _get_users_col, add_new_user, get_user_wrapper
from database.utils import coll
from .dbprint import print_collection

test_username = 'Taras'
test_track_name = 'jogging'

def run_all_trackable_tests():
    StartDate_ReturnsNone_IfNotSet()
    StartDate_SetsValue_IfNotPresent()
    StartDate_PutValue_EqOrig()
    SetStartDate_Updates_PresentValue()
    print("\n")

    GetBounds_ReturnsNone_IfNotSet()
    SetBounds_SetsValues_IfNotPresent()
    SetBounds_UpdatesValues_IfPresent()
    Bounds_PutValue_EqOrig()
    print("\n")

    AddEntry_AddsNewDoc()
    GetEntries_ReturnsAllNonMetadataDocs()
    GetNLastEntries_ReturnsNResults()
    GetNLastEntries_ResultSortedDescending()
    AddEntry_ExistsDoc_WithArgValues()

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

def StartDate_SetsValue_IfNotPresent():
    _set_up()
    tr = _track_test_instance()

    orig = datetime.utcnow()
    tr.set_start_date(orig)

    assert tr.get_start_date() != None
    _log_passed()

def SetStartDate_Updates_PresentValue():
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

    tr.add_user_entry(datetime.utcnow(), 42)
    assert tr.get_bounds() is None
    _log_passed()

def SetBounds_SetsValues_IfNotPresent():
    _set_up()
    tr = _track_test_instance()

    tr.set_bounds(1, 10)

    assert tr.get_bounds() is not None
    _log_passed()
    
def SetBounds_UpdatesValues_IfPresent():
    _set_up()
    tr = _track_test_instance()

    tr.set_bounds(1, 10)

    new_min = 42;
    new_max = 43;
    tr.set_bounds(new_min, new_max)

    assert tr.get_bounds() == (new_min, new_max)
    _log_passed()
    
def Bounds_PutValue_EqOrig():
    _set_up()
    tr = _track_test_instance()

    min, max = 42, 43
    tr.set_bounds(min, max)

    assert tr.get_bounds() == (min, max)
    _log_passed()
    

#endregion

#region entries
def AddEntry_AddsNewDoc():
    _set_up()
    tr = _track_test_instance()

    count_before = _test_track_coll().count()
    tr.add_user_entry(datetime.utcnow(), None)
    count_after = _test_track_coll().count()

    assert count_after == count_before + 1
    _log_passed()

def GetEntries_ReturnsAllNonMetadataDocs():
    _set_up()
    tr = _track_test_instance()
    tr.add_user_entry(datetime.utcnow(), 42)
    tr.add_user_entry(datetime.utcnow(), 42)
    
    count = _test_track_coll().find({}).count() - 1 # -1 for metadata

    entries = tr.get_user_entries()

    assert len(entries) == count
    _log_passed()

def GetNLastEntries_ReturnsNResults():
    _set_up()
    tr = _track_test_instance()
    tr.add_user_entry(datetime.utcnow(), 42)
    tr.add_user_entry(datetime.utcnow(), 42)
    tr.add_user_entry(datetime.utcnow(), 42)
    

    entries = tr.get_user_entries(2)

    assert len(entries) == 2
    _log_passed()

def GetNLastEntries_ResultSortedDescending():
    _set_up()
    tr = _track_test_instance()
    tr.add_user_entry(datetime.utcnow(), 42)
    tr.add_user_entry(datetime.utcnow(), 42)
    tr.add_user_entry(datetime.utcnow(), 42)
    

    entries = tr.get_user_entries(2)

    assert sorted([entry['date'] for entry in entries], reverse=True)
    _log_passed()

def AddEntry_ExistsDoc_WithArgValues():
    _set_up()
    tr = _track_test_instance()

    date = datetime.fromtimestamp(1000000)
    val = 42
    tr.add_user_entry(date, val)

    assert {
        'date' : date,
        'value' : val
    } in tr.get_user_entries()
    _log_passed()

#endregion


def _set_up():
    _get_users_col().remove({})
    _test_track_coll().remove({})

    new_us_wrapper = add_new_user(test_username)
    new_us_wrapper.register_trackable(test_track_name)

def _track_test_instance():
    return get_user_wrapper(test_username).get_trackable_wrapper(test_track_name)

def _log_passed():
    print('passed test: {0}'.format(stack()[1][3]))  

def _test_track_coll():
    return  coll(_trackable_coll_name(test_username, test_track_name))
