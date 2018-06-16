import os
import random
import threading
import time

from dht.bucket_set import BucketSet
from dht.dht_request_handler import DHTRequestHandler
from dht.dht_server import DHTServer
from dht.peer import Peer
from dht.shortlist import Shortlist
from dht.utils import Utils

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

K_BUCKET_SIZE = 20 if os.getenv("K_BUCKET_SIZE") is None else int(os.getenv("K_BUCKET_SIZE"))
ALPHA = 3 if os.getenv("ALPHA") is None else int(os.getenv("ALPHA"))
ID_BITS = 128 if os.getenv("ID_BITS") is None else int(os.getenv("ID_BITS"))
ITERATION_SLEEP = 1 if os.getenv("ITERATION_SLEEP") is None else int(os.getenv("ITERATION_SLEEP"))


class DHT:
    def __init__(self,
                 host,
                 port,
                 id=None,
                 seeds=None,
                 storage=None,
                 info=None,
                 hash_function=Utils.hash_function,
                 requesthandler=DHTRequestHandler):
        """
        Initialises a new distributed hash table
        :param host: hostname of this here table
        :param port: listening port of the current table
        :param id: id of the current table
        :param seeds: seeds present in the table
        :param storage: shelf to be used by the table
        :param info:
        :param hash_function: hash function used to compute the ids
        :param requesthandler: handles requests from other nodes in the network
        """
        if info is None:
            info = {}
        if storage is None:
            storage = {}
        if seeds is None:
            seeds = []
        if not id:
            id = Utils.random_id()
        self.storage = storage
        self.info = info
        self.hash_function = hash_function
        self.peer = Peer(host, port, id, info)
        self.data = self.storage
        self.buckets = BucketSet(K_BUCKET_SIZE, ID_BITS, self.peer.id)
        self.rpc_ids = {}  # should probably have a lock for this
        self.server = DHTServer(self.peer.address(), requesthandler)
        self.server.dht = self
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        self.bootstrap(seeds)

    def identity(self):
        """
        Returns the nodeid on the network
        :return: nodeid on the network
        """
        return self.peer.id

    def iterative_find_nodes(self, key, boot_peer=None):
        shortlist = Shortlist(K_BUCKET_SIZE, key)
        shortlist.update(self.buckets.nearest_nodes(key, limit=ALPHA))
        if boot_peer:
            rpc_id = random.getrandbits(ID_BITS)
            self.rpc_ids[rpc_id] = shortlist
            boot_peer.find_node(key, rpc_id, socket=self.server.socket, peer_id=self.peer.id, peer_info=self.peer.info)
        while (not shortlist.complete()) or boot_peer:
            nearest_nodes = shortlist.get_next_iteration(ALPHA)
            for peer in nearest_nodes:
                shortlist.mark(peer)
                rpc_id = random.getrandbits(ID_BITS)
                self.rpc_ids[rpc_id] = shortlist
                peer.find_node(key, rpc_id, socket=self.server.socket, peer_id=self.peer.id, peer_info=self.info)
            time.sleep(ITERATION_SLEEP)
            boot_peer = None
        return shortlist.results()

    def iterative_find_value(self, key):
        shortlist = Shortlist(K_BUCKET_SIZE, key)
        shortlist.update(self.buckets.nearest_nodes(key, limit=ALPHA))
        while not shortlist.complete():
            nearest_nodes = shortlist.get_next_iteration(ALPHA)
            for peer in nearest_nodes:
                shortlist.mark(peer)
                rpc_id = random.getrandbits(ID_BITS)
                self.rpc_ids[rpc_id] = shortlist
                peer.find_value(key,
                                rpc_id,
                                socket=self.server.socket,
                                peer_id=self.peer.id,
                                peer_info=self.info)
            time.sleep(ITERATION_SLEEP)
        return shortlist.completion_result()

    # Return the list of connected peers
    def peers(self):
        return self.buckets.to_dict()

    def bootstrap(self, bootstrap_nodes=None):
        """
        Bootstrap the network with a list of bootstrap nodes
        :param bootstrap_nodes: A list of nodes to bootstrap the network with
        :return: None
        """
        if bootstrap_nodes is None:
            bootstrap_nodes = []
        for bnode in bootstrap_nodes:
            boot_peer = Peer(bnode[0], bnode[1], "", "")
            self.iterative_find_nodes(self.peer.id, boot_peer=boot_peer)

        if len(bootstrap_nodes) == 0:
            for bnode in self.buckets.to_list():
                self.iterative_find_nodes(self.peer.id, boot_peer=Peer(bnode[0], bnode[1], bnode[2], bnode[3]))

    def get_sync(self, key, handler):
        """
        Get a value in a sync way, calling an handler
        :param key: Key we are searching for
        :param handler: Handler to pass value to after getting the key
        :return:
        """
        try:
            d = self[key]
        except:
            d = None

        handler(d)

    def get(self, key, handler):
        """
        Get a value in async way
        :param key: Key we are searching for
        :param handler:
        :return: Handler to pass value to after getting the key
        """
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
