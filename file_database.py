import json
import pickle
import os
import logging

import win32file

from dict_database import DictDatabase
import win32event

FILE_PATH = 'database.pkl'

class FileDatabase(DictDatabase):
    def __init__(self):
        """
        Initializes an instance of the FileDatabase class, extending DictDatabase.
        Loads an existing dictionary from a file or initializes a new one if the file does not exist.
        """
        super().__init__()
        self.create_file()  # Load data when initializing, if file exists.
        logging.info("FileDatabase initialized.")
        print("FileDatabase initialized.")

    def create_file(self):
        """
        Creates a new file with an empty dictionary if the file doesn't exist.
        """
        self.handle = win32file.CreateFile(
            FILE_PATH,
            win32file.GENERIC_WRITE | win32file.GENERIC_READ,
            win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE,
            None,
            win32file.OPEN_ALWAYS,  # Overwrite the file if it exists
            0,
            None)

    def save(self):
        """
        Saves the current dictionary state to a file.

        :return: None
        :rtype: None
        """
        # with open(FILE_PATH, 'wb') as database_file:
        #     pickle.dump(self.dict, database_file)
        # logging.info("Database saved to file.")
        # print("Database saved to file.")

        data = json.dumps(self.dict).encode('utf-8')  # Convert dict to bytes
        win32file.SetFilePointer(self.handle, 0, win32file.FILE_BEGIN)  # Move to the beginning of the file
        win32file.SetEndOfFile(self.handle)  # Ensure the file is truncated before writing new data
        win32file.WriteFile(self.handle, data)
        print(f"Data saved to file: {data}")

    # def load(self):
    #     """
    #     Loads the dictionary state from a file, if it exists. If the file does not exist,
    #     initializes with an empty dictionary.
    #
    #     :return: None
    #     :rtype: None
    #     """
    #     if os.path.exists(FILE_PATH):
    #         with open(FILE_PATH, 'rb') as database_file:
    #             self.dict = pickle.load(database_file)
    #         logging.info("Database loaded from file.")
    #         print("Database loaded from file.")
    #     else:
    #         logging.warning("Database file not found. Initialized with an empty dictionary.")
    #         print("Database file not found. Initialized with an empty dictionary.")
    #         self.dict = {}

    def load(self):
        if os.path.exists(FILE_PATH):
            win32file.SetFilePointer(self.handle, 0, win32file.FILE_BEGIN)  # Start from the beginning of the file
            result, data = win32file.ReadFile(self.handle, 1024)  # Read up to 1024 bytes
            # print(f"Data read from file: {data}")
            if result != 0 or not data:  # If no data was read or data is empty
                self.dict = {}  # Initialize the dictionary as empty
            else:
                try:
                    self.dict = json.loads(data.decode('utf-8'))  # Convert bytes back to dict
                except json.JSONDecodeError:
                    # print("Error: Invalid JSON in file.")
                    self.dict = {}  # Initialize as empty if JSON is invalid

    def set_value(self, val, key):
        """
        Sets a value in the dictionary for a specified key, then saves the updated dictionary to the file.

        :param val: The value to store in the dictionary.
        :type val: any
        :param key: The key to associate with the value.
        :type key: str
        :return: True if the operation is successful, False otherwise.
        :rtype: bool
        """
        response = super().set_value(val, key)
        if response:
            self.save()  # Save to file after updating
        return response

    def get_value(self, key):
        """
        Retrieves the value associated with the specified key in the dictionary, after loading the dictionary from the file.

        :param key: The key for which to retrieve the value.
        :type key: str
        :return: The value associated with the key if it exists, otherwise None.
        :rtype: any or None
        """
        val = super().get_value(key)
        logging.info(f"Returning value: {val} for key: {key}")
        print(f"Returning value: {val} for key: {key}")
        return val

    def delete_value(self, key):
        """
        Deletes the key-value pair associated with the specified key from the dictionary, then saves the updated dictionary to the file.

        :param key: The key of the key-value pair to delete.
        :type key: str
        :return: The value associated with the deleted key if it exists, otherwise None.
        :rtype: any or None
        """
        val = super().delete_value(key)
        if val is not None:
            self.save()  # Save to file after deletion
        logging.info(f"Deleted key-value pair for key: {key}. Value: {val}")
        print(f"Deleted key-value pair for key: {key}. Value: {val}")
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
    assert db.get_value('b') is None, "Non-existent key 'b' should return None"

    # Test delete_value
    assert db.delete_value('a') == 20, "Failed to delete key 'a'"
    assert db.get_value('a') is None, "Key 'a' should be deleted and return None"

    # Test delete_value for non-existent key
    assert db.delete_value('b') is None, "Deleting non-existent key 'b' should return None"

    logging.info("All assertions passed.")
    print("All assertions passed.")
