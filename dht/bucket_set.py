import heapq
import threading

from dht.peer import Peer
from dht.utils import Utils


class BucketSet:
    def __init__(self, k, id_bits, id):
        """
        Initialises a set of k-buckets. Kademlia stores a list up to k in size for each of the node ids bits.
        A 128 bit id has 128 such lists. Each list contains triple information (ip_address, udp_port, node-id)
        :param k: The bucket size is a constant ,k, which caps the size of the lists within a k bucket
        , normally k=20.
        :param id_bits: Bits in the nodeid.
        :param id: The peer id
        """
        self.id = id  # the unique nodes id
        self.bucket_size = k  # lists are >= k
        self.buckets = [list() for _ in range(id_bits)]  # create lists as large as the bits of the nodeid
        self.lock = threading.Lock()

    def to_list(self):
        """
        Converts k-buckets to list object. Returns this list object
        :return: A list representation of the buckets
        """
        l = []
        for bucket in self.buckets:
            l += bucket
        return l

    def to_dict(self):
        """
        Converts k-buckets to list object. Returns this list object
        :return: Returns a dict representation
        """
        l = []
        for bucket in self.buckets:
            for peer in bucket:
                if len(peer) == 4:
                    l.append({'host': peer[0], 'port': peer[1], 'id': peer[2], 'info': peer[3]})
        return l

    def insert(self, peer):
        """
        Adds a peer into a k-bucket
        :param peer: A participant within the network.
        :return: None
        """
        if peer.id != self.id:
            bucket_number = Utils.largest_differing_bit(self.id, peer.id)
            peer_triple = peer.astriple()
            with self.lock:
                bucket = self.buckets[bucket_number]
                if peer_triple in bucket:
                    bucket.pop(bucket.index(peer_triple))
                elif len(bucket) >= self.bucket_size:
                    bucket.pop(0)
                bucket.append(peer_triple)

    def nearest_nodes(self, key, limit=None):
        num_results = limit if limit else self.bucket_size
        with self.lock:
            def keyfunction(peer):
                # ideally there would be a better way with names?
                # Instead of storing triples it would be nice to have a dict
                return key ^ peer[2]

            peers = (peer for bucket in self.buckets for peer in bucket)
            best_peers = heapq.nsmallest(self.bucket_size, peers, keyfunction)
            return [Peer(*peer) for peer in best_peers]
