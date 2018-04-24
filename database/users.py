from .utils import DatabaseConsts as dc, get_users_col
from pymongo import MongoClient
from pymongo.collection import Collection

# class UserAlreadyExistsError:
#         def __init__(self, message):
#             self.message = message

#         def __str__(self):
#             return repr(self.message)


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
    '''
    # assert isinstance(dc.USERS_COLL_NAME, MongoClient)

    new_user = {
        'name' : user_name,
        'trackables' : []
    }

    users_coll = get_users_col()

    users_coll.insert_one(new_user)


def get_user(user_name):
    '''
    get's the user dict : {
        name : 'string',
        trackables : [string arr]
    }
    returns None if no doc with user_name is present in db
    '''

    users_coll = get_users_col()
    return users_coll.find_one({'name' : user_name})


def user_registered(user_name):
    '''
    returns true if 1 or more user docs with user_name are present in db
    '''
    assert _users_with_name(user_name) <= 1

    return _users_with_name(user_name) == 1


def _users_with_name(user_name):
    return get_users_col().find({'name' : user_name}).count()















    






