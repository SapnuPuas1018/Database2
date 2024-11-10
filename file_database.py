import pickle
import os
import logging
from dict_database import DictDatabase

FILE_PATH = 'database.pkl'

class FileDatabase(DictDatabase):
    def __init__(self):
        super().__init__()
        logging.info("Initializing FileDatabase.")
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, 'wb') as database_file:
                pickle.dump(self.dict, database_file)  # Initialize with an empty dictionary
            logging.info("FileDatabase initialized with an empty dictionary.")
        else:
            with open(FILE_PATH, 'x') as database_file:
                pickle.dump(self.dict, database_file)
            logging.info("FileDatabase created a new database file with an empty dictionary.")

    def save(self):
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, 'wb') as database_file:
                pickle.dump(self.dict, database_file)
            logging.info("Database saved to file.")

    def load(self):
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, 'rb') as database_file:
                self.dict = pickle.load(database_file)
            logging.info("Database loaded from file.")
        else:
            self.dict = {}
            logging.warning("Database file not found. Initialized with an empty dictionary.")

    def set_value(self, val, key):
        self.load()
        response = super().set_value(val, key)
        self.save()
        return response

    def get_value(self, key):
        self.load()
        val = super().get_value(key)
        logging.info(f"Returning value: {val} for key: {key}")
        return val

    def delete_value(self, key):
        self.load()
        val = super().delete_value(key)
        self.save()
        return val


if __name__ == '__main__':
    # Set up logging
    logging.basicConfig(filename='file_database.log', level=logging.DEBUG)

    # Test cases with assertions
    db = FileDatabase()

    # Test set_value
    assert db.set_value(10, 'a') == True, "Failed to set key 'a'"
    assert db.get_value('a') == 10, "Failed to get value for key 'a'"

    # Test update value
    assert db.set_value(20, 'a') == True, "Failed to update key 'a'"
    assert db.get_value('a') == 20, "Failed to get updated value for key 'a'"

    # Test get_value for non-existent key
    assert db.get_value('b') == None, "Non-existent key 'b' should return None"

    # Test delete_value
    assert db.delete_value('a') == 20, "Failed to delete key 'a'"
    assert db.get_value('a') == None, "Key 'a' should be deleted and return None"

    # Test delete_value for non-existent key
    assert db.delete_value('b') == None, "Deleting non-existent key 'b' should return None"

    logging.info("All assertions passed.")
    print("All assertions passed.")