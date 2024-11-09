import threading
import multiprocessing
from sync_database import SyncDatabase


class ProcessTest():
    def __init__(self):
        self.process_list = []  # Threads list
        self.data_base = SyncDatabase('multiprocessing')


    def test_1(self):
        # Write Test
        self.data_base.set_value('complete', 'test 1')


    def test_2(self):
        # Read Test
        return self.data_base.get_value('test 1')


    def test_3(self):
        # Read then Write Test
        process = multiprocessing.Process(target=self.data_base.get_value, args=('test 3',))
        process.start()
        self.process_list.append(process)

        process = multiprocessing.Process(target=self.data_base.set_value, args=('complete', 'test 3'))
        process.start()
        self.process_list.append(process)

        for process in self.process_list:
            process.join()


    def test_4(self):
        # Write then Read Test
        thread = multiprocessing.Process(target=self.data_base.set_value, args=('complete', 'test 4'))
        thread.start()
        self.process_list.append(thread)

        thread = multiprocessing.Process(target=self.data_base.get_value, args=('test 4',))
        thread.start()
        self.process_list.append(thread)

        for thread in self.process_list:
            thread.join()


    def test_5(self):
        # Multiple Reads Test
        for i in range(1, 15):
            thread = multiprocessing.Process(target=self.data_base.get_value, args=('test 5',))
            thread.start()
            self.process_list.append(thread)

        for thread in self.process_list:
            thread.join()


    def test_6(self):
        # Multiple Reads Test
        for i in range(1, 7):
            process = multiprocessing.Process(target=self.data_base.get_value, args=('test 6',))
            process.start()
            self.process_list.append(process)

        process = multiprocessing.Process(target=self.data_base.set_value, args=('complete 1', 'test 6'))
        process.start()
        self.process_list.append(process)

        for i in range(1, 7):
            process = multiprocessing.Process(target=self.data_base.get_value, args=('test 6',))
            process.start()
            self.process_list.append(process)

        for process in self.process_list:
            process.join()


    def test_7(self):
        # Multiple Reads, then multiple Writes Test
        for i in range(1, 3):
            process = multiprocessing.Process(target=self.data_base.get_value, args=('test 7',))
            process.start()
            self.process_list.append(process)

        process = multiprocessing.Process(target=self.data_base.set_value, args=('complete 1', 'test 7'))
        process.start()
        self.process_list.append(process)

        process = multiprocessing.Process(target=self.data_base.set_value, args=('complete 2', 'test 7'))
        process.start()
        self.process_list.append(process)

        for process in self.process_list:
            process.join()


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
    test = ProcessTest()
    test.test_all()
