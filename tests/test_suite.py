import unittest

from tests.dht_test import DHTTest
from tests.peer_test import PeerTest


def test_suite():
    suite = unittest.TestSuite()

    suite.addTests([PeerTest, DHTTest])
