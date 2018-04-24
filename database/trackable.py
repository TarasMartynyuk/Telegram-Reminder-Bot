from .utils import DatabaseConsts as dc
from pymongo import MongoClient
from pymongo.collection import Collection 
from datetime import datetime

class TrackableDbWrapper:

    def __init__(self, username, name):
        self.username = username
        self.name = name
        self.coll_name = _trackable_coll_name(username, name)


    def get_start_date(self):
        timestamp =  _trackable_metadata_doc(self.coll_name)['date']
        return datetime.fromtimestamp(timestamp)
    
    def set_start_date(self, new_date):
        '''
        new_date is datatime of trackable creation, in UTC
        '''
        if not isinstance(new_date, datetime):
            raise TypeError('new_date must be a datetime')

        timestamp = new_date.timestamp()

        _trackable_coll(self.coll_name).update_one({
            'date' : { '$exists' : True }
            }, { 
                '$set' : {'date' : timestamp
            }}, 
            upsert=True)


    def get_bounds(self):
        pass

    def set_bounds(self, new_bounds):
        pass



#region helpers
def _trackable_coll_name(username, name):
    '''
    get's the collection identifier for the user's trackable, 
    distinct from all other user's trackables
    '''
    return username + name

def _trackable_coll(coll_name):
    return dc.CLIENT[dc.DATABASE_NAME][coll_name]

def _trackable_metadata_doc(coll_name):
    return _trackable_coll(coll_name).find_one({
            'date' : { '$exists' : True }
        })
#endregion
    


    

