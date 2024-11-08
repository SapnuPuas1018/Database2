
from sync_database import SyncDatabase
def main():
    database = SyncDatabase()
    print(database.set_value('val1','key1'))
    print(database.dict)
    print(database.get_value('key1'))


if __name__ == '__main__':
    main()
