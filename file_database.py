import pickle
from dict_database import DictDatabase


class FileDatabase(DictDatabase):
    def __init__(self):
        super().__init__()
        self.db = open('database.pkl')

    def set_value(self, val, key):
        self.dict = pickle.load(self.db)
        response = super().set_value(val, key)
        pickle.dump(self.db, self.dict)
        return response

    def get_value(self, key):
        self.dict = pickle.load(self.db)
        return super().get_value(key)

    def delete_value(self, key):
        self.dict = pickle.load(self.db)
        super().delete_value(key)
        pickle.dump(self.db, self.dict)