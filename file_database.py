import pickle
import os
from dict_database import DictDatabase

FILE_PATH = 'database.pkl'
class FileDatabase(DictDatabase):
    def __init__(self):
        super().__init__()
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, 'wb') as database_file:
                pickle.dump(self.dict, database_file)  # Initialize with an empty dictionary
        else:
            with open(FILE_PATH, 'x') as database_file:
                pickle.dump(self.dict, database_file)

    def save(self):
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, 'wb') as database_file:
                pickle.dump(self.dict, database_file)   # Initialize with an empty dictionary

    def load(self):
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, 'rb') as database_file:
                self.dict = pickle.load(database_file)
        else:
            self.dict = {}

    def set_value(self, val, key):
        self.load()
        response = super().set_value(val, key)
        self.save()
        return response

    def get_value(self, key):
        self.load()
        val = super().get_value(key)
        print('returning ' + str(val))
        return val

    def delete_value(self, key):
        self.load()
        val = super().delete_value(key)
        self.save()
        return val

def main():
    db = FileDatabase()
    db.set_value('val', 'key')
    print(db.get_value('key'))
    print(db.dict)


if __name__ == '__main__':
    main()
