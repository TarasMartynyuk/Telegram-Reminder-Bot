from .utils import DatabaseConsts as dc
from .trackable import TrackableDbWrapper, drop_trackable_collection
from pymongo import MongoClient
from pymongo.collection import Collection

#region static
def init():
    '''
    run this before using this module any further
    adds the uniqueness constraint on users id field
    '''
    # _get_users_col().drop_indexes()
    _get_users_col().create_index( 'id', unique = True)

def add_new_user(id, username):
    '''
    adds a new user doc {
        id : id,
        name : user_name,
        trackables : [empty]
    } to db
    raises DuplicateKeyError if user with user_name already exists
    returns the UserDbWrapper obj for created user 
    '''
    new_user_doc = {
        'id' : id,
        'name' : username,
        'trackables' : []
    }

    users_coll = _get_users_col()
    users_coll.insert_one(new_user_doc)

    return UserDbWrapper(new_user_doc)

def get_user_wrapper(id):
    '''
    returns the UserDbWrapper obj 
    returns None if no doc present
    '''
    user_doc = _get_users_col().find_one({'id' : id})

    return None if user_doc == None \
        else UserDbWrapper(user_doc)
    
def user_registered(id):
    '''
    returns true if 1 or more user docs with user_name are present in db
    '''
    assert _users_with_id(id) <= 1
    return _users_with_id(id) == 1

#endregion

class UserDbWrapper:

    def __init__(self, doc):
        # name, as in db docs
        self.name = doc['name']
        # string array - names of all the user's trackables 
        self.trackable_names = doc['trackables']
        self.id = doc['id']

    def get_trackable_wrapper(self, name): 
        '''
        returns TrackableDbWrapper obj that manages the corresponding trackable collection
        if name is not present in user's trackablenames None is returned
        '''
        return None \
            if (name not in self.trackable_names) \
            else TrackableDbWrapper(self.name, name)

    def trackable_registered(self, name):
        return name in self.trackable_names

    def register_trackable(self, name):
        '''
        adds the name to self.trackables, and writes it to the db user doc
        '''
        if self.trackable_registered(name):
            raise ValueError('trackable already registered')

        self.trackable_names.append(name)
        _get_users_col().update_one({
            'name' : self.name}, {
            '$set' : {
                'trackables' : self.trackable_names
            }
        })

    def delete_trackable(self, name):
        '''
        deletes the entire trackable's collection,
        and removes it's name from this user's doc
        and this wrappers trackablenames list
        '''
        if not self.trackable_registered(name):
            raise ValueError('trackable must be registered')

        drop_trackable_collection(self.name, name)

        self.trackable_names.remove(name)
        _get_users_col().update_one({
            'id' : self.id
            }, {
                '$set' : {
                    'trackables' : self.trackable_names
                }
            })

#region helpers

def _get_users_col():
    return dc.CLIENT[dc.DATABASE_NAME][dc.USERS_COLL_NAME]

def _users_with_id(id):
    return _get_users_col().find({'id' : id}).count()
#endregion













    






