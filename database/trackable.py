from .utils import DatabaseConsts as dc
from pymongo import MongoClient
from pymongo.collection import Collection 
from datetime import datetime

class TrackableDbWrapper:

    def __init__(self, username, name):
        self.username = username
        self.name = name
        self.coll_name = _trackable_coll_name(username, name)
        _insert_empty_metadata(self.coll_name)


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

        min = metadata_doc.get('min_val', None)
        max = metadata_doc.get('max_val', None)

        if min is None or max is None:
            return None

        return (min, max)

    def set_bounds(self, min, max):

        _update_trackable_metadata_doc(
            self.coll_name, {
                '$set' : {
                    'min_val' : min,
                    'max_val' : max
                }
            })




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
    return _trackable_coll(coll_name).find_one({
            'date' : { '$exists' : True }
        })

def _insert_empty_metadata(coll_name):
    _trackable_coll(coll_name).insert_one({
        'date' : None,
        'min' : None,
        'max' : None
    })

def _update_trackable_metadata_doc(coll_name, update):
    _trackable_coll(coll_name).update_one({
        'date' : { '$exists' : True }
        }, update, 
        upsert=True)
#endregion
    


    

