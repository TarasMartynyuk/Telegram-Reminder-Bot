from pymongo import MongoClient

class DatabaseConsts:

    CLIENT = MongoClient()
    DATABASE_NAME = "Reminder-Bot"
    USERS_COLL_NAME = "Users"

