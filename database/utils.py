from pymongo import MongoClient

class DatabaseConsts:

    CLIENT = MongoClient("mongodb://mdbu:pwwp@cluster0-shard-00-00-tkafr.mongodb.net:27017,cluster0-shard-00-01-tkafr.mongodb.net:27017," + 
        "cluster0-shard-00-02-tkafr.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
    DATABASE_NAME = "Reminder-Bot"
    USERS_COLL_NAME = "Users"
    MIN_VAL = 'min_val'
    MAX_VAL = 'max_val'

def coll(coll_name):
    return DatabaseConsts.CLIENT \
        [DatabaseConsts.DATABASE_NAME][coll_name]