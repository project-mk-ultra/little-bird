import heapq
import threading

from dht.peer import Peer
from dht.utils import Utils


class BucketSet(object):
    def __init__(self, bucket_size, buckets, id):
        self.id = id
        self.bucket_size = bucket_size
        self.buckets = [list() for _ in range(buckets)]
        self.lock = threading.Lock()

    def to_list(self):
        l = []
        for bucket in self.buckets: l += bucket
        return l

    def to_dict(self):
        l = []
        for bucket in self.buckets:
            for peer in bucket:
                if len(peer) == 4:
                    l.append({'host': peer[0], 'port': peer[1], 'id': peer[2], 'info': peer[3]})
        return l

    def insert(self, peer):
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
