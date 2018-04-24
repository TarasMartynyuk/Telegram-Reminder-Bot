from .utils import DatabaseConsts as dc
from pymongo import MongoClient
from pymongo.collection import Collection

#region static
def init():
    '''
    run this before using this module any further
    adds the uniqueness constraint on users field
    '''
    _get_users_col().create_index( 'user_name', unique = True)

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
        pass

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


#region helpers

def _get_users_col():
    return dc.CLIENT[dc.DATABASE_NAME][dc.USERS_COLL_NAME]


def _users_with_name(user_name):
    return _get_users_col().find({'name' : user_name}).count()
#endregion













    






