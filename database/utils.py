from pymongo import MongoClient

class DatabaseConsts:

    CLIENT = MongoClient()
    DATABASE_NAME = "Reminder-Bot"
    USERS_COLL_NAME = "Users"

def get_users_col():
    return DatabaseConsts.CLIENT\
    [DatabaseConsts.DATABASE_NAME][DatabaseConsts.USERS_COLL_NAME]