import multiprocessing
import threading
from threading import Thread, Lock, Semaphore
from multiprocessing import Process, Lock, Semaphore, Value


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
            self.write_semaphores = threading.Lock()
            self.sem = threading.Semaphore(MAX_READERS)

            self.reader_count_lock = threading.Lock()
            self.reader_count = 0
        elif self.mode == 'multiprocessing':
            self.write_lock = multiprocessing.Lock()
            self.sem = multiprocessing.Semaphore(MAX_READERS)

            self.reader_count_lock = multiprocessing.Lock()
            self.reader_count = Value('i', 0)  # Shared integer for reader count
        else:
            print('|:-(')
            raise ValueError("Mode must be either 'threading' or 'multiprocessing'.")





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
        if self.mode == 'threading':
            with self.reader_count_lock:
                self.reader_count += 1
                if self.reader_count == 1:
                    self.write_lock.acquire()  # First reader locks writing
        elif self.mode == 'multiprocessing':
            with self.reader_count_lock:
                self.reader_count.value += 1
                if self.reader_count.value == 1:
                    self.write_lock.acquire()



    def end_read(self):
        if self.mode == 'threading':
            with self.reader_count_lock:
                self.reader_count -= 1
                if self.reader_count == 0:
                    self.write_lock.release()  # Last reader unlocks writing
        elif self.mode == 'multiprocessing':
            with self.reader_count_lock:
                self.reader_count.value -= 1
                if self.reader_count.value == 0:
                    self.write_lock.release()
        self.sem.release()


    def delete_value(self, key):
        with self.write_lock:
            time.sleep(5)   # Simulate writing time
            val = super().delete_value(key)
            logging.debug(f'Deleted - {key}: {val}')
        return val
