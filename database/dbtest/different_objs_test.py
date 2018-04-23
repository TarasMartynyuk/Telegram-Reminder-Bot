from pymongo import MongoClient
import copy as cp
from database.private import utils as ut

DB_NAME = 'db'
COLLECTION_NAME = 'collection'

def list_all():
    mongo_cl = MongoClient()
    ut.print_collection(mongo_cl[DB_NAME][COLLECTION_NAME])

def put_diff_objs():
    mongo_cl = MongoClient()
    col =  mongo_cl[DB_NAME][COLLECTION_NAME]
    col.remove({})

    single_doc = {
        'col-wide-field' : 'value' 
    }

    one_of_may_doc = {
        'one_of_many_field' : 'value'
    }

    col.insert_one(single_doc)
    # col.insert_many(
    #     [ one_of_may_doc, 
    #       one_of_may_doc, 
    #       one_of_may_doc ])
    col.insert_one(one_of_may_doc)
    col.insert_one(cp.deepcopy(one_of_may_doc))
    

def retrieve_singular():
    mongo_cl = MongoClient()
    col =  mongo_cl[DB_NAME][COLLECTION_NAME]


    single = col.find_one({'col-wide-field' : 'value' })

    print(single)



