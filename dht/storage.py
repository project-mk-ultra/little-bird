import shelve


class Shelve:
    """
    It works like Python 2s pickle
    """
    def __init__(self, f):
        """
        Initialises a shelf for object persistence against instances
        :param f: file path pointing to external file shelf should use
        """
        self.shelve = shelve.open(f)

    def dump(self):
        """
        Shows all saved keys within the file
        :return: stdout output of all keys in the shelf
        """
        for x in self.shelve:
            print('key:', x, '\t\tvalue:', self.shelve[x])

    def __getitem__(self, key):
        """
        Gets a key within the shelf
        :param key: Specifies the key of the object within the shelf
        :return: Returns a value from the shelf
        """
        return self.shelve[str(key)]

    def __setitem__(self, key, value):
        """
        Sets a key and its respective value into the shelf.
        :param key: Key for later reindexing
        :param value: Value to save
        :return: None
        """
        self.shelve[str(key)] = value

    def __contains__(self, key):
        """
        Checks whether a key exists in the shelf.
        :param key: Specifies the key to check
        :return: Key if it exists
        """
        return str(key) in self.shelve
