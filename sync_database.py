import multiprocessing
import threading
from multiprocessing import Value
import time
import logging
from file_database import FileDatabase
import win32event

MAX_READERS = 10
logging.basicConfig(filename='sync_database.log', level=logging.DEBUG)


class SyncDatabase(FileDatabase):
    def __init__(self, mode):
        """
        Initializes an instance of the SyncDatabase class, extending FileDatabase.
        Sets up synchronization primitives for either threading or multiprocessing modes.

        :param mode: The mode of synchronization, either 'threading' or 'multiprocessing'.
        :type mode: str
        :raises ValueError: If an invalid mode is specified.
        """
        super().__init__()
        self.mode = mode
        logging.info(f"Initializing SyncDatabase in {mode} mode.")
        print(f"Initializing SyncDatabase in {mode} mode.")

        if self.mode == 'threading':
            self.write_lock = win32event.CreateMutex(None, False, 'WriteLock')
            self.sem_lock = win32event.CreateMutex(None, False, 'SemLock')
            self.sem = threading.Semaphore(MAX_READERS)
            self.reader_count_lock = win32event.CreateMutex(None, False, 'ReaderCountLock')
            self.reader_count = 0
        elif self.mode == 'multiprocessing':
            self.write_lock = win32event.CreateMutex(None, False, 'WriteLock')
            self.sem_lock = win32event.CreateMutex(None, False, 'SemLock')
            self.sem = multiprocessing.Semaphore(MAX_READERS)
            self.reader_count_lock = win32event.CreateMutex(None, False, 'ReaderCountLock')
            self.reader_count = Value('i', 0)  # Shared integer for reader count
        else:
            logging.error("Invalid mode specified.")
            print("Invalid mode specified.")
            raise ValueError("Mode must be either 'threading' or 'multiprocessing'.")

    def catch_all_semaphores(self):
        """
        Acquires all reader semaphores, blocking additional read access to the database.

        :return: None
        :rtype: None
        """
        win32event.WaitForSingleObject(self.sem_lock, -1)
        print("Acquiring semaphores...")
        for _ in range(10):
            self.sem.acquire()

    def release_all_semaphores(self):
        """
        Releases all reader semaphores, allowing read access to the database.

        :return: None
        :rtype: None
        """
        for _ in range(10):
            self.sem.release()
        win32event.ReleaseMutex(self.sem_lock)
        print("Released all semaphores.")

    def set_value(self, val, key):
        """
        Sets a value in the database for a specified key, ensuring exclusive write access.

        :param val: The value to store in the database.
        :param key: The key to associate with the value.
        :return: True if the operation is successful, False otherwise.
        """
        self.catch_all_semaphores()
        logging.info(f"Attempting to set {key} to {val}.")
        print(f"Attempting to set {key} to {val}.")
        win32event.WaitForSingleObject(self.write_lock, -1)
        # time.sleep(5)  # Simulate writing time
        response = super().set_value(val, key)
        logging.debug(f'Write - {key}: {val}')
        print(f'Write - {key}: {val}')
        win32event.ReleaseMutex(self.write_lock)
        self.release_all_semaphores()
        return response

    def get_value(self, key):
        """
        Retrieves the value associated with the specified key in the dictionary, ensuring safe concurrent read access.

        :param key: The key for which to retrieve the value.
        :type key: str
        :return: The value associated with the key if it exists, otherwise None.
        :rtype: any or None
        """
        logging.info(f"Attempting to get value for {key}.")
        print(f"Attempting to get value for {key}.")
        self.get_read_access()
        # time.sleep(5)  # Simulate reading time
        val = super().get_value(key)
        logging.debug(f'Read - {key}: {val}')
        print(f'Read - {key}: {val}')
        self.end_read()
        return val

    def get_read_access(self):
        """
        Requests read access for a reader, acquiring the necessary locks based on the mode.
        The first reader in a series will acquire the write lock, blocking writers.

        :return: None
        :rtype: None
        """
        logging.info("Requesting read access.")
        print("Requesting read access.")
        self.sem.acquire()
        if self.mode == 'threading':
            win32event.WaitForSingleObject(self.reader_count_lock, -1)
            self.reader_count += 1
            if self.reader_count == 1:
                logging.info("First reader acquiring write lock.")
                print("First reader acquiring write lock.")
                win32event.WaitForSingleObject(self.write_lock, -1)  # First reader locks writing
            win32event.ReleaseMutex(self.reader_count_lock)
        elif self.mode == 'multiprocessing':
            win32event.WaitForSingleObject(self.reader_count_lock, -1)
            self.reader_count.value += 1
            if self.reader_count.value == 1:
                logging.info("First reader acquiring write lock (multiprocessing).")
                print("First reader acquiring write lock (multiprocessing).")
                win32event.WaitForSingleObject(self.write_lock, -1)
            win32event.WaitForSingleObject(self.write_lock, -1)  # First reader locks writing


    def end_read(self):
        """
        Ends read access for a reader, releasing locks as necessary based on the mode.
        The last reader in a series will release the write lock, allowing writers.

        :return: None
        :rtype: None
        """
        logging.info("Ending read access.")
        print("Ending read access.")
        if self.mode == 'threading':
            win32event.WaitForSingleObject(self.reader_count_lock, -1)
            self.reader_count -= 1
            if self.reader_count == 0:
                logging.info("Last reader releasing write lock.")
                print("Last reader releasing write lock.")
                win32event.ReleaseMutex(self.write_lock)  # Last reader unlocks writing
            win32event.ReleaseMutex(self.reader_count_lock)
        self.sem.release()

    def delete_value(self, key):
        """
        Deletes the key-value pair associated with the specified key from the dictionary, ensuring exclusive write access.
        Synchronizes access based on the mode and saves the updated dictionary to the file.

        :param key: The key of the key-value pair to delete.
        :type key: str
        :return: The value associated with the deleted key if it exists, otherwise None.
        :rtype: any or None
        """
        self.catch_all_semaphores()
        logging.info(f"Attempting to delete {key}.")
        print(f"Attempting to delete {key}.")
        win32event.WaitForSingleObject(self.write_lock, -1)
        # time.sleep(5)  # Simulate writing time
        val = super().delete_value(key)
        logging.debug(f'Deleted - {key}: {val}')
        print(f'Deleted - {key}: {val}')
        win32event.ReleaseMutex(self.write_lock)
        self.release_all_semaphores()
        return val


if __name__ == '__main__':
    # Set up a SyncDatabase in threading mode for testing
    db = SyncDatabase('threading')
    # Assertions and testing in threading mode
    assert db.set_value(100, 'test_key') == True, "Failed to set 'test_key'"
    assert db.get_value('test_key') == 100, "Failed to retrieve 'test_key'"
    assert db.delete_value('test_key') == 100, "Failed to delete 'test_key'"
    assert db.get_value('test_key') is None, "Deleted key 'test_key' should return None"

    # Set up a SyncDatabase in multiprocessing mode for testing
    db_multiprocess = SyncDatabase('multiprocessing')
    assert db_multiprocess.set_value(200, 'another_key') == True, "Failed to set 'another_key'"
    assert db_multiprocess.get_value('another_key') == 200, "Failed to retrieve 'another_key'"
    assert db_multiprocess.delete_value('another_key') == 200, "Failed to delete 'another_key'"
    assert db_multiprocess.get_value('another_key') is None, "Deleted key 'another_key' should return None"

    logging.info("All assertions passed in both threading and multiprocessing modes.")
    print("All assertions passed in both threading and multiprocessing modes.")
