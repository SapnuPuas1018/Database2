import multiprocessing
from file_database import FileDatabase


class SyncDatabase(FileDatabase):
    def __init__(self):
        super().__init__()
        