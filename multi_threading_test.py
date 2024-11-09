import threading
from sync_database import SyncDatabase


class ThreadingTest():
    def __init__(self):
        self.threads_list = []
        self.data_base = SyncDatabase('threading')


    def test_1(self):
        # Write Test
        self.data_base.set_value('complete', 'test 1')


    def test_2(self):
        # Read Test
        return self.data_base.get_value('test 1')


    def test_3(self):
        # Read then Write Test
        thread = threading.Thread(target=self.data_base.get_value, args=('test 3',))
        thread.start()
        self.threads_list.append(thread)

        thread = threading.Thread(target=self.data_base.set_value, args=('complete', 'test 3'))
        thread.start()
        self.threads_list.append(thread)

        for thread in self.threads_list:
            thread.join()


    def test_4(self):
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
        # Multiple Reads Test
        for i in range(1, 15):
            thread = threading.Thread(target=self.data_base.get_value, args=('test 5',))
            thread.start()
            self.threads_list.append(thread)

        for thread in self.threads_list:
            thread.join()


    def test_6(self):
        # Multiple Reads Test, while writing request
        for i in range(1, 7):
            thread = threading.Thread(target=self.data_base.get_value, args=('test 6',))
            thread.start()
            self.threads_list.append(thread)

        thread = threading.Thread(target=self.data_base.set_value, args=('complete 1', 'test 6'))
        thread.start()
        self.threads_list.append(thread)

        for i in range(1, 7):
            thread = threading.Thread(target=self.data_base.get_value, args=('test 6',))
            thread.start()
            self.threads_list.append(thread)

        for thread in self.threads_list:
            thread.join()


    def test_7(self):
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
