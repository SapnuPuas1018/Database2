import multiprocessing
import threading
from threading import Thread, Lock, Semaphore
from multiprocessing import Process, Lock, Semaphore


import time
import logging
from file_database import FileDatabase


MAX_READERS = 10
logging.basicConfig(filename='DataBase.log', level=logging.DEBUG)


class SyncDatabase(FileDatabase):
    def __init__(self, mode):
        super().__init__()
        self.mode = mode
        if self.mode == 'threading':
            self.write_lock = threading.Lock()
            self.sem = threading.Semaphore(MAX_READERS)

            self.reader_count_lock = threading.Lock()
        elif self.mode == 'multiprocessing':
            self.write_lock = multiprocessing.Lock()
            self.sem = multiprocessing.Semaphore(MAX_READERS)

            self.reader_count_lock = multiprocessing.Lock()
        else:
            print('|:-(')

        self.reader_count = 0


    def set_value(self, val, key):
        with self.write_lock:
            time.sleep(5) # Simulate writing time
            val = super().set_value(val, key)
        return val


    def get_value(self, key):
        self.get_read_access()
        time.sleep(5)  # Simulate reading time
        val = super().get_value(key)
        logging.debug(f'Read - {key}: {val}')
        self.end_read()
        return val

    def get_read_access(self):
        self.sem.acquire()
        with self.reader_count_lock:
            self.reader_count += 1
            if self.reader_count == 1:  # first reader locks writing
                self.write_lock.acquire()



    def end_read(self):
        with self.reader_count_lock:
            self.reader_count -= 1
            if self.reader_count == 0:
                self.write_lock.release()  # Last reader unlocks writing
        self.sem.release()


    def delete_value(self, key):
        with self.write_lock:
            time.sleep(5)   # Simulate writing time
            val = super().delete_value(key)
            logging.debug(f'Deleted - {key}: {val}')
        return val
