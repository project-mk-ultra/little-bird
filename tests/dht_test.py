import unittest

from dht.dht import DHT


class DHTTest(unittest.TestCase):
    """
    Tests key lookups with a single table
    """
    def test_dht(self):
        dht = DHT("localhost", 9789)

        dht['foo'] = 'bar'

        self.assertEqual(dht["foo"], "bar")

    def test_multiple_dht(self):
        """
        Tests key lookups with multiple tables
        """
        dht1 = DHT("localhost", 9789)
        dht1["fizz"] = "buzz"
        for i in range(10):
            host, port = "localhost", 9788 - i
            dht = DHT("localhost", port, seeds=[("localhost", 9789)])
            self.assertEqual(dht["fizz"], "buzz")
