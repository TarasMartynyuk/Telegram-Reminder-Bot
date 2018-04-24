from .utils import DatabaseConsts as dc, get_users_col
from pymongo import MongoClient
from pymongo.collection import Collection

#region static
def init():
    '''
    run this before using this module any further
    adds the uniqueness constraint on users field
    '''
    get_users_col().create_index( 'user_name', unique = True)


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

    users_coll = get_users_col()
    users_coll.insert_one(new_user_doc)

    return UserDbWrapper(new_user_doc)

def user_registered(user_name):
    '''
    returns true if 1 or more user docs with user_name are present in db
    '''
    assert _users_with_name(user_name) <= 1

    return _users_with_name(user_name) == 1

def _users_with_name(user_name):
    return get_users_col().find({'name' : user_name}).count()
#endregion

class UserDbWrapper:

    def __init__(self, doc):
        # name, as in db docs
        self.user_name = doc['name']
        # string array - names of all the user's trackables 
        self.trackables = doc['trackables']

    def get_trackables(self):
        '''
        get's the list of all user's trackables:
            [string arr]
        returns None if such user is present in db
        '''

        users_coll = get_users_col()
        return users_coll.find_one({'name' : self.user_name})['trackables']

    
    def get_trackable_wrapper(self, name):
        '''
        name must be present in self.trackables,
        returns TrackableDbWrapper obj that manages the corresponding collection
        '''
        pass

    def add_new_trackable(self, name):
        pass

















    






