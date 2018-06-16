import unittest
from pathlib import Path

from dht.peer import Peer


class PeerTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_peer(self):
        peer = Peer("localhost", 9789, "foo", "bar")
        self.assertEqual(str(peer), "localhost:9789")
