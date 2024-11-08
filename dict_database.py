

class DictDatabase:
    def __init__(self):
        self.dict = {}

    def set_value(self, val, key):
        try:
            self.dict[key] = val
            return True
        except KeyError:
            return False

    def get_value(self, key):
        print(self.dict)
        print(self.dict.keys())
        if key in self.dict.keys():
            print('111')
            return self.dict[key]
        print('2222')
        return None

    def delete_value(self, key):
        if key in self.dict.keys():
            return self.dict.pop(key)


def main():
    db = DictDatabase()
    db.set_value('val', 'key')
    print(db.get_value('key'))
    db.delete_value('key')
    print(db.dict)


if __name__ == '__main__':
    main()
