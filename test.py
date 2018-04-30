from database.dbtest.test import *
from database.dbtest.dbprint import *
from database.users import *
from database.trackable import drop_trackable_collection
from database.utils import DatabaseConsts as dc

def main():
    print('all users: ')
    print_all_users()
    # test_all()

    # dc.CLIENT[dc.DATABASE_NAME]['TheUnicornStripper--sample_trackable'].drop()
    put_sample_data(382338945, "sample trackable")
    # print_all_colls()


    print_all_trackable_entries(382338945)
    # print_all_trackable_entries(get_user_wrapper(382338945))

if __name__ == "__main__":
    main()

