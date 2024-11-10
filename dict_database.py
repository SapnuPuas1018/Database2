import logging

logging.basicConfig(filename='dict_database.log', level=logging.DEBUG)

class DictDatabase:
    def __init__(self):
        self.dict = {}
        logging.info("Initialized DictDatabase with an empty dictionary.")

    def set_value(self, val, key):
        try:
            self.dict[key] = val
            logging.info(f"set_value: Set {key} = {val}")
            return True
        except KeyError:
            logging.error(f"Failed to set {key} = {val}")
            return False

    def get_value(self, key):
        logging.info(f"get_value: Attempting to retrieve {key}")
        if key in self.dict.keys():
            logging.info(f"get_value: Found {key} = {self.dict[key]}")
            return self.dict[key]
        logging.warning(f"get_value: {key} not found.")
        return None

    def delete_value(self, key):
        logging.info(f"delete_value: Attempting to delete {key}")
        if key in self.dict.keys():
            value = self.dict.pop(key)
            logging.info(f"delete_value: Deleted {key} = {value}")
            return value
        logging.warning(f"delete_value: {key} not found for deletion.")
        return None


if __name__ == '__main__':

    # Test cases with assertions
    db = DictDatabase()

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