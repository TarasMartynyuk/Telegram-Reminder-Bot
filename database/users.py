from .utils import DatabaseConsts as dc
from .trackable import TrackableDbWrapper, drop_trackable_collection
from pymongo import MongoClient
from pymongo.collection import Collection

#region static
def init():
    '''
    run this before using this module any further
    adds the uniqueness constraint on users field
    '''
    _get_users_col().drop_indexes()
    # _get_users_col().create_index( 'user_name', unique = False)

def add_new_user(user_name):
    '''
    adds a new user doc {
        name : user_name,
        trackables : [empty]
    } to db
    raises DuplicateKeyError if user with user_name already exists
    returns the UserDbWrapper obj for created user 
    '''
    new_user_doc = {
        'name' : user_name,
        'trackables' : []
    }

    users_coll = _get_users_col()
    users_coll.insert_one(new_user_doc)

    return UserDbWrapper(new_user_doc)

def get_user_wrapper(user_name):
    '''
    returns the UserDbWrapper obj 
    returns None if no doc present
    '''
    user_doc = _get_users_col().find_one({'name' : user_name})

    return None if user_doc == None \
        else UserDbWrapper(user_doc)
    
def user_registered(user_name):
    '''
    returns true if 1 or more user docs with user_name are present in db
    '''
    assert _users_with_name(user_name) <= 1
    # assert 1 < 0
    print("_users_with_name(user_name) " + str(_users_with_name(user_name)))
    return _users_with_name(user_name) == 1

#endregion

class UserDbWrapper:

    def __init__(self, doc):
        # name, as in db docs
        self.name = doc['name']
        # string array - names of all the user's trackables 
        self.trackable_names = doc['trackables']

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

#region helpers

def _get_users_col():
    return dc.CLIENT[dc.DATABASE_NAME][dc.USERS_COLL_NAME]

def _users_with_name(user_name):
    return _get_users_col().find({'name' : user_name}).count()
#endregion













    






