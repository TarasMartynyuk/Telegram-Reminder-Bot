from database.utils import DatabaseConsts as dc
from pymongo.collection import Collection


def print_collection(collection):

    assert isinstance(collection, Collection)

    cursor = collection.find({})

    has_smth = False
    for document in cursor:
          print(document)
          has_smth = True

    if not has_smth:
        print (f'no documents in {collection.name}')





def print_all_users():
    print_collection(dc.CLIENT[dc.DATABASE_NAME][dc.USERS_COLL_NAME])


def print_all_docs(client, db_name, col_name):
    
    col = client[db_name][col_name]
    print_collection(col)

