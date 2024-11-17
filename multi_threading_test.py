import threading
from sync_database import SyncDatabase

class ThreadingTest:
    def __init__(self):
        """
        Initializes an instance of the ThreadingTest class.
        Sets up a list to manage threads and a SyncDatabase instance in 'threading' mode.

        :return: None
        :rtype: None
        """
        self.threads_list = []
        self.data_base = SyncDatabase('threading')


    def test_1(self):
        """
        Executes a write test by setting a value in the database.

        :return: None
        :rtype: None
        """
        # Write Test
        self.data_base.set_value('complete', 'test 1')


    def test_2(self):
        """
        Executes a read test by retrieving a value from the database.

        :return: The value associated with the key 'test 1' if it exists, otherwise None.
        :rtype: any or None
        """
        # Read Test
        return self.data_base.get_value('test 1')


    def test_3(self):
        """
        Executes a test to read and then write a value concurrently.
        Starts separate threads to perform a read and a write operation and waits for them to complete.

        :return: None
        :rtype: None
        """
        thread = threading.Thread(target=self.data_base.get_value, args=('test 3',))
        thread.start()
        self.threads_list.append(thread)

        thread = threading.Thread(target=self.data_base.set_value, args=('complete', 'test 3'))
        thread.start()
        self.threads_list.append(thread)

        for thread in self.threads_list:
            thread.join()


    def test_4(self):
        """
        Executes a test to write and then read a value concurrently.
        Starts separate threads to perform a write and a read operation and waits for them to complete.

        :return: None
        :rtype: None
        """
        # Write then Read Test
        thread = threading.Thread(target=self.data_base.set_value, args=('complete', 'test 4'))
        thread.start()
        self.threads_list.append(thread)

        thread = threading.Thread(target=self.data_base.get_value, args=('test 4',))
        thread.start()
        self.threads_list.append(thread)

        for thread in self.threads_list:
            thread.join()


    def test_5(self):
        """
        Executes a test with multiple read requests on the same key.
        Starts multiple threads to perform read operations and waits for them to complete.

        :return: None
        :rtype: None
        """
        for i in range(1, 15):
            thread = threading.Thread(target=self.data_base.get_value, args=('test 5',))
            thread.start()
            self.threads_list.append(thread)

        for thread in self.threads_list:
            thread.join()


    def test_6(self):
        """
        Executes a test with multiple concurrent read requests and one write request on the same key.
        Starts multiple threads to perform read operations, one to perform a write operation, and waits for all to complete.

        :return: None
        :rtype: None
        """
        for i in range(1, 7):
            thread = threading.Thread(target=self.data_base.get_value, args=('test 6',))
            thread.start()
            self.threads_list.append(thread)


        thread = threading.Thread(target=self.data_base.set_value, args=('complete', 'test 6'))
        thread.start()
        self.threads_list.append(thread)


        for i in range(1, 7):
            thread = threading.Thread(target=self.data_base.get_value, args=('test 6',))
            thread.start()
            self.threads_list.append(thread)

        for thread in self.threads_list:
            thread.join()


    def test_7(self):
        """
        Executes a test with multiple read requests followed by multiple write requests on the same key.
        Starts multiple threads to perform read and write operations, and waits for them to complete.

        :return: None
        :rtype: None
        """
        # Multiple Reads, then multiple Writes Test
        for i in range(1, 3):
            thread = threading.Thread(target=self.data_base.get_value, args=('test 7',))
            thread.start()
            self.threads_list.append(thread)

        thread = threading.Thread(target=self.data_base.set_value, args=('complete 1', 'test 7'))
        thread.start()
        self.threads_list.append(thread)

        thread = threading.Thread(target=self.data_base.set_value, args=('complete 2', 'test 7'))
        thread.start()
        self.threads_list.append(thread)

        for thread in self.threads_list:
            thread.join()


    def test_all(self):
        """
        Runs all tests sequentially to test the database in various read and write concurrency scenarios.

        :return: None
        :rtype: None
        """
        # Commence all Tests
        print('-----------------------------------start test 1-----------------------------------')
        self.test_1()
        print('-----------------------------------start test 2-----------------------------------')
        self.test_2()
        print('-----------------------------------start test 3-----------------------------------')
        self.test_3()
        print('-----------------------------------start test 4-----------------------------------')
        self.test_4()
        print('-----------------------------------start test 5-----------------------------------')
        self.test_5()
        print('-----------------------------------start test 6-----------------------------------')
        self.test_6()
        print('-----------------------------------start test 7-----------------------------------')
        self.test_7()


if __name__ == '__main__':
    test = ThreadingTest()
    test.test_all()
