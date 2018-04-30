from database.dbtest.test import *
from database.dbtest.dbprint import *
from database.users import *
from database.trackable import drop_trackable_collection
from database.utils import DatabaseConsts as dc

def main():
    # test_all()

    # dc.CLIENT[dc.DATABASE_NAME]['TheUnicornStripper--sample_trackable'].drop()
    # put_sample_data(382338945, "playing with my cat")
    # print_all_colls()

    # get_user_wrapper(382338945).delete_trackable('playing with my cat')


    # get_user_wrapper(382338945).register_trackable("playing with my cat")
    # print('all users: ')
    # print_all_users()
    print_all_trackable_entries(382338945)
    # print_all_trackable_entries(get_user_wrapper(382338945))

if __name__ == "__main__":
    main()

