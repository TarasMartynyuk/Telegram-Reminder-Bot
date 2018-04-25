from database.utils import DatabaseConsts as dc
from datetime import datetime
from database.trackable import TrackableDbWrapper, _trackable_coll_name
from database.utils import coll
# from .dbprint import print_collection
from .utils import *


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
    set_up()
    tr = track_test_instance()

    assert tr.get_start_date() is None
    log_passed()

def StartDate_PutValue_EqOrig():
    set_up()
    tr = track_test_instance()

    orig = datetime.utcnow()
    tr.set_start_date(orig)

    assert orig == tr.get_start_date()
    log_passed()

def StartDate_SetsValue_IfNotPresent():
    set_up()
    tr = track_test_instance()

    orig = datetime.utcnow()
    tr.set_start_date(orig)

    assert tr.get_start_date() != None
    log_passed()

def SetStartDate_Updates_PresentValue():
    set_up()
    tr = track_test_instance()
    assert datetime.utcnow() == datetime.utcnow()

    first = datetime.utcnow()
    tr.set_start_date(first)

    second = datetime.fromtimestamp(
        datetime.utcnow().timestamp() + 100000
    )
    
    tr.set_start_date(second)

    assert tr.get_start_date() == second
    log_passed()
#endregion

#region bounds
def GetBounds_ReturnsNone_IfNotSet():
    set_up()
    tr = track_test_instance()

    tr.add_user_entry(datetime.utcnow(), 42)
    assert tr.get_bounds() is None
    log_passed()

def SetBounds_SetsValues_IfNotPresent():
    set_up()
    tr = track_test_instance()

    tr.set_bounds(1, 10)

    assert tr.get_bounds() is not None
    log_passed()
    
def SetBounds_UpdatesValues_IfPresent():
    set_up()
    tr = track_test_instance()

    tr.set_bounds(1, 10)

    new_min = 42;
    new_max = 43;
    tr.set_bounds(new_min, new_max)

    assert tr.get_bounds() == (new_min, new_max)
    log_passed()
    
def Bounds_PutValue_EqOrig():
    set_up()
    tr = track_test_instance()

    min, max = 42, 43
    tr.set_bounds(min, max)

    assert tr.get_bounds() == (min, max)
    log_passed()
    

#endregion

#region entries
def AddEntry_AddsNewDoc():
    set_up()
    tr = track_test_instance()

    count_before = test_track_coll().count()
    tr.add_user_entry(datetime.utcnow(), None)
    count_after = test_track_coll().count()

    assert count_after == count_before + 1
    log_passed()

def GetEntries_ReturnsAllNonMetadataDocs():
    set_up()
    tr = track_test_instance()
    tr.add_user_entry(datetime.utcnow(), 42)
    tr.add_user_entry(datetime.utcnow(), 42)
    
    count = test_track_coll().find({}).count() - 1 # -1 for metadata

    entries = tr.get_user_entries()

    assert len(entries) == count
    log_passed()

def GetNLastEntries_ReturnsNResults():
    set_up()
    tr = track_test_instance()
    tr.add_user_entry(datetime.utcnow(), 42)
    tr.add_user_entry(datetime.utcnow(), 42)
    tr.add_user_entry(datetime.utcnow(), 42)
    

    entries = tr.get_user_entries(2)

    assert len(entries) == 2
    log_passed()

def GetNLastEntries_ResultSortedDescending():
    set_up()
    tr = track_test_instance()
    tr.add_user_entry(datetime.utcnow(), 42)
    tr.add_user_entry(datetime.utcnow(), 42)
    tr.add_user_entry(datetime.utcnow(), 42)
    

    entries = tr.get_user_entries(2)

    assert sorted([entry['date'] for entry in entries], reverse=True)
    log_passed()

def AddEntry_ExistsDoc_WithArgValues():
    set_up()
    tr = track_test_instance()

    date = datetime.fromtimestamp(1000000)
    val = 42
    tr.add_user_entry(date, val)

    assert {
        'date' : date,
        'value' : val
    } in tr.get_user_entries()
    log_passed()

#endregion




