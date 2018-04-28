from database.utils import DatabaseConsts as dc, coll
from pymongo.collection import Collection

def print_all_colls():
    db = dc.CLIENT[dc.DATABASE_NAME]
    print('database : {0}'.format(dc.DATABASE_NAME) + ' {')

    for collname in db.collection_names():
        print("\t\"{0}\" : {1}".format(collname, coll(collname).count({})))

    print('}')
    
def print_all_users():
    _print_collection(dc.CLIENT[dc.DATABASE_NAME][dc.USERS_COLL_NAME])

def print_all_trackable_entries(user):
    print('User : {0}: '.format(user.name))

    for tr in user.trackable_names:
        _print_collection(coll(
            user.get_trackable_wrapper(tr).coll_name
        ))
        
    print('}')


def _print_collection(collection):

    assert isinstance(collection, Collection)
    print(collection.name)
    cursor = collection.find({})

    has_smth = False
    for document in cursor:
          print('\t' + str(document))
          has_smth = True

    if not has_smth:
        print (f'no documents in {collection.name}')