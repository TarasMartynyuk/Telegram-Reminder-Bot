from .utils import DatabaseConsts as dc
import pymongo
from pymongo.collection import Collection 
from datetime import datetime

class TrackableDbWrapper:

    def __init__(self, username, name):
        self.username = username
        self.name = name
        self.coll_name = _trackable_coll_name(username, name)
        _create_empty_metadata_if_not_present(self.coll_name)

    #region metadata
    def get_start_date(self):
        '''
        returns None if data not set
        '''
        metadata_doc = _get_trackable_metadata_doc(self.coll_name)
        timestamp =  metadata_doc.get('date', None)

        if timestamp is None:
            return None

        return datetime.fromtimestamp(timestamp)
    
    def set_start_date(self, new_date):
        '''
        new_date is datatime of trackable creation, in UTC
        '''
        if not isinstance(new_date, datetime):
            raise TypeError('new_date must be a datetime')

        timestamp = new_date.timestamp()

        _update_trackable_metadata_doc(
            self.coll_name, { 
                '$set' : {'date' : timestamp
            }})

    def get_bounds(self):
        '''
        return value is a tuple :
        ( min : val,
            max : val)
        returns None if not set
        '''
        metadata_doc = _get_trackable_metadata_doc(self.coll_name)

        min = metadata_doc.get(dc.MIN_VAL, None)
        max = metadata_doc.get(dc.MAX_VAL, None)

        if min is None or max is None:
            return None

        return (min, max)

    def set_bounds(self, min, max):

        _update_trackable_metadata_doc(
            self.coll_name, {
                '$set' : {
                    dc.MIN_VAL : min,
                    dc.MAX_VAL : max
                }
            })
    #endregion

    def add_user_entry(self, date, value):

        if not isinstance(date, datetime):
            raise TypeError('date must be a datetime')

        _trackable_coll(self.coll_name).insert_one({ 
            'date' : date.timestamp(),
            'value' : value
        })

    # TODO: remove querying for n-1 elems!
    # mb use separate col for metadata?
    def get_user_entries(self, n_last_to_take=0):
        '''
        returns list of {
            'date' : datetime,
            'value' : int
        }
        '''
        all_entries = _trackable_coll(self.coll_name).find({
            # 'value' : { '$exists' : True }
            dc.MAX_VAL : { '$exists' : False }
        }, )

        n_last = all_entries.sort("date", pymongo.DESCENDING). \
            limit(n_last_to_take)

        return [{
            'date' : datetime.fromtimestamp(entry['date']),
            'value' : entry['value']
        } for entry in n_last ]



#region helpers
def _trackable_coll_name(username, name):
    '''
    get's the collection identifier for the user's trackable, 
    distinct from all other user's trackables
    '''
    return username + name

def _trackable_coll(coll_name):
    return dc.CLIENT[dc.DATABASE_NAME][coll_name]

def _get_trackable_metadata_doc(coll_name):
    return _trackable_coll(coll_name).find_one(_metadata_query())

def _create_empty_metadata_if_not_present(coll_name):
    _trackable_coll(coll_name).update_one(_metadata_query(), {
        '$set' : {
            'date' : None,
            dc.MIN_VAL : None,
            dc.MAX_VAL : None
        }}, 
    upsert=True)

def _metadata_query():
    return {
        'date' : { '$exists' : True },
        dc.MIN_VAL : { '$exists' : True },
        dc.MAX_VAL : { '$exists' : True }
    }

def _update_trackable_metadata_doc(coll_name, update):
    _trackable_coll(coll_name).update_one({
        'date' : { '$exists' : True }
        }, update, 
        upsert=True)
#endregion
    


    

