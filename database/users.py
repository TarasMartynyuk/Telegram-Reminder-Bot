from .utils import DatabaseConsts as dc, get_users_col
from pymongo import MongoClient
from pymongo.collection import Collection

def add_new_user(user_name):
    '''
    adds a new user doc {
        name : user_name,
        trackables : [empty]
    } to db
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
    user with that name must be present in collection
    '''
    users_coll = get_users_col()

    assert users_coll.find({'name' : user_name}).count() == 1

    return users_coll.find_one({'name' : user_name})


def user_registered(user_name):
    '''
    returns whether the user with username is registered in db
    '''

    pass















    






