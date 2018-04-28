from database.dbtest.test import *
from database.dbtest.dbprint import *
from database.users import *

def main():
    # print('all users: ')
    # print_all_users()


    print_all_trackable_entries(get_user_wrapper(382338945))
    # drop_users()
    # print_all_colls()

    # drop_db()
    # test_all()

if __name__ == "__main__":
    main()

