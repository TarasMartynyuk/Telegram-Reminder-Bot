from pymongo import MongoClient

class DatabaseConsts:

    CLIENT = MongoClient()
    DATABASE_NAME = "Reminder-Bot"
    USERS_COLL_NAME = "Users"
    MIN_VAL = 'min_val'
    MAX_VAL = 'max_val'

def coll(coll_name):
    return DatabaseConsts.CLIENT \
        [DatabaseConsts.DATABASE_NAME][coll_name]