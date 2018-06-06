import shelve


def test():
    pass


class Shelve:
    def __init__(self, f):
        self.shelve = shelve.open(f)

    def dump(self):
        for x in self.shelve:
            print('key:', x, '\t\tvalue:', self.shelve[x])

    def __getitem__(self, key):
        return self.shelve[str(key)]

    def __setitem__(self, key, value):
        self.shelve[str(key)] = value

    def __contains__(self, key):
        return str(key) in self.shelve
