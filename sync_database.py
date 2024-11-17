import win32event
import win32api
import win32con
import logging
from file_database import FileDatabase

MAX_READERS = 10
logging.basicConfig(filename='sync_database.log', level=logging.DEBUG)

class SyncDatabase(FileDatabase):
    def __init__(self, mode):
        """
        Initializes an instance of the SyncDatabase class, extending FileDatabase.
        Uses win32event objects for synchronization with threading or multiprocessing.
        """
        super().__init__()
        self.mode = mode
        logging.info(f"Initializing SyncDatabase in {mode} mode.")

        if self.mode == 'threading':
            self.sem_lock = win32event.CreateMutex(None, False, None)
            self.sem = win32event.CreateSemaphore(None, MAX_READERS, MAX_READERS, None)
        elif self.mode == 'multiprocessing':
            # Create a named global mutex
            self.sem_lock = win32event.CreateMutex(None, False, "Global\\MyGlobalMutex")
            if not self.sem_lock:
                raise Exception("Failed to create or open the global mutex.")
            self.sem = win32event.CreateSemaphore(None, MAX_READERS, MAX_READERS, "Global\\MyGlobalSemaphore")
            if not self.sem:
                raise Exception("Failed to create or open the global semaphore.")
        else:
            logging.error("Invalid mode specified.")
            raise ValueError("Mode must be either 'threading' or 'multiprocessing'.")

    def catch_all_semaphores(self):
        """
        Acquires all reader semaphores, blocking additional read access.
        """
        win32event.WaitForSingleObject(self.sem_lock, win32event.INFINITE)
        for _ in range(MAX_READERS):
            win32event.WaitForSingleObject(self.sem, win32event.INFINITE)
            print(f'sem number {_ + 1} acquired')

    def release_all_semaphores(self):
        """
        Releases all reader semaphores, allowing read access.
        """
        for _ in range(MAX_READERS):
            win32event.ReleaseSemaphore(self.sem, 1)
            print('sem released')
        win32event.ReleaseMutex(self.sem_lock)

    def set_value(self, val, key):
        """
        Writes a value to the database with exclusive access.
        """
        self.catch_all_semaphores()
        logging.info(f"Attempting to set {key} to {val}.")
        response = super().set_value(val, key)
        logging.debug(f'Write - {key}: {val}')
        self.release_all_semaphores()
        return response

    def get_value(self, key):
        """
        Reads a value from the database with shared read access.
        """
        logging.info(f"Attempting to get value for {key}.")
        self.get_read_access()
        val = super().get_value(key)
        logging.debug(f'Read - {key}: {val}')
        self.end_read()
        return val

    def get_read_access(self):
        """
        Requests read access.
        """
        logging.info("Requesting read access.")
        win32event.WaitForSingleObject(self.sem, win32event.INFINITE)

    def end_read(self):
        """
        Ends read access.
        """
        logging.info("Ending read access.")
        win32event.ReleaseSemaphore(self.sem, 1)

    def delete_value(self, key):
        """
        Deletes a key-value pair with exclusive access.
        """
        self.catch_all_semaphores()
        logging.info(f"Attempting to delete {key}.")
        val = super().delete_value(key)
        logging.debug(f'Deleted - {key}: {val}')
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
