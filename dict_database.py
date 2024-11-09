

class DictDatabase:
    def __init__(self):
        self.dict = {}

    def set_value(self, val, key):
        try:
            self.dict[key] = val
            print('set_value, DictDatabase, dict: ' + str(self.dict))
            return True
        except KeyError:
            return False

    def get_value(self, key):
        print('get_value, DictDatabase, dict: ' + str(self.dict))
        if key in self.dict.keys():
            return self.dict[key]
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
