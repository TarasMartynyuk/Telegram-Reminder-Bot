from database.dbtest.test import *
from database.dbtest.dbprint import *
from database.users import _get_users_col
from database.trackable import drop_trackable_collection
from database.utils import DatabaseConsts as dc

def main():
    test_all()

if __name__ == "__main__":
    main()

