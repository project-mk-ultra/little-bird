import random
import threading
import time

from dht import hashing
from dht.bucket_set import BucketSet
from dht.dht_request_handler import DHTRequestHandler
from dht.dht_server import DHTServer
from dht.hashing import random_id, id_bits
from dht.peer import Peer
from dht.shortlist import Shortlist

k = 20
alpha = 3
id_bits = 128
iteration_sleep = 1


class DHT:
    def __init__(self,
                 host,
                 port,
                 id=None,
                 seeds=[],
                 storage={},
                 info={},
                 hash_function=hashing.hash_function,
                 requesthandler=DHTRequestHandler):
        if not id:
            id = random_id()
        self.storage = storage
        self.info = info
        self.hash_function = hash_function
        self.peer = Peer(host, port, id, info)
        self.data = self.storage
        self.buckets = BucketSet(k, id_bits, self.peer.id)
        self.rpc_ids = {}  # should probably have a lock for this
        self.server = DHTServer(self.peer.address(), requesthandler)
        self.server.dht = self
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        self.bootstrap(seeds)

    def identity(self):
        return self.peer.id

    def iterative_find_nodes(self, key, boot_peer=None):
        shortlist = Shortlist(k, key)
        shortlist.update(self.buckets.nearest_nodes(key, limit=alpha))
        if boot_peer:
            rpc_id = random.getrandbits(id_bits)
            self.rpc_ids[rpc_id] = shortlist
            boot_peer.find_node(key, rpc_id, socket=self.server.socket, peer_id=self.peer.id, peer_info=self.peer.info)
        while (not shortlist.complete()) or boot_peer:
            nearest_nodes = shortlist.get_next_iteration(alpha)
            for peer in nearest_nodes:
                shortlist.mark(peer)
                rpc_id = random.getrandbits(id_bits)
                self.rpc_ids[rpc_id] = shortlist
                peer.find_node(key, rpc_id, socket=self.server.socket, peer_id=self.peer.id, peer_info=self.info)
            time.sleep(iteration_sleep)
            boot_peer = None
        return shortlist.results()

    def iterative_find_value(self, key):
        shortlist = Shortlist(k, key)
        shortlist.update(self.buckets.nearest_nodes(key, limit=alpha))
        while not shortlist.complete():
            nearest_nodes = shortlist.get_next_iteration(alpha)
            for peer in nearest_nodes:
                shortlist.mark(peer)
                rpc_id = random.getrandbits(id_bits)
                self.rpc_ids[rpc_id] = shortlist
                peer.find_value(key,
                                rpc_id,
                                socket=self.server.socket,
                                peer_id=self.peer.id,
                                peer_info=self.info)
            time.sleep(iteration_sleep)
        return shortlist.completion_result()

    # Return the list of connected peers
    def peers(self):
        return self.buckets.to_dict()

    # Boostrap the network with a list of bootstrap nodes
    def bootstrap(self, bootstrap_nodes=[]):
        for bnode in bootstrap_nodes:
            boot_peer = Peer(bnode[0], bnode[1], "", "")
            self.iterative_find_nodes(self.peer.id, boot_peer=boot_peer)

        if len(bootstrap_nodes) == 0:
            for bnode in self.buckets.to_list():
                self.iterative_find_nodes(self.peer.id, boot_peer=Peer(bnode[0], bnode[1], bnode[2], bnode[3]))

    # Get a value in a sync way, calling an handler
    def get_sync(self, key, handler):
        try:
            d = self[key]
        except:
            d = None

        handler(d)

    # Get a value in async way
    def get(self, key, handler):
        # print ('dht.get',key)
        t = threading.Thread(target=self.get_sync, args=(key, handler))
        t.start()

    # Iterator
    def __iter__(self):
        return map(lambda key: int(key), self.data.__iter__())

    # Operator []
    def __getitem__(self, key):
        if type(key) == int:
            hashed_key = key
        else:
            hashed_key = self.hash_function(key)

        if str(hashed_key) in self.data:
            return self.data[str(hashed_key)]
        result = self.iterative_find_value(hashed_key)
        if result:
            return result
        raise KeyError

    # Operator []=
    def __setitem__(self, key, value):
        hashed_key = self.hash_function(key)
        # print ('dht.set',key,value,hashed_key)
        nearest_nodes = self.iterative_find_nodes(hashed_key)
        if not nearest_nodes:
            self.data[str(hashed_key)] = value
        for node in nearest_nodes:
            node.store(hashed_key, value, socket=self.server.socket, peer_id=self.peer.id)

    def tick(self):

        pass
