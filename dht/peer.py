import json


class Peer:
    """ DHT Peer Information """

    def __init__(self, host, port, id, info):
        self.host, self.port, self.id, self.info = host, port, id, info

    def address(self):
        return self.host, self.port

    def send_message(self, message, sock=None, peer_id=None, peer_info=None, lock=None):
        message["peer_id"] = peer_id
        message["peer_info"] = peer_info
        encoded = json.dumps(message)
        if sock:
            if lock:
                with lock:
                    sock.sendto(encoded.encode('utf-8'), (self.host, self.port))
            else:
                sock.sendto(encoded.encode('utf-8'), (self.host, self.port))

    def ping(self, socket=None, peer_id=None, peer_info=None, lock=None):
        message = {
            "message_type": "ping"
        }
        self.send_message(message, socket, peer_id, peer_info, lock)

    def pong(self, socket=None, peer_id=None, peer_info=None, lock=None):
        message = {
            "message_type": "pong"
        }
        self.send_message(message, socket, peer_id, peer_info, lock)

    def store(self, key, value, socket=None, peer_id=None, peer_info=None, lock=None):
        message = {
            "message_type": "store",
            "id": key,
            "value": value
        }
        self.send_message(message, socket, peer_id, peer_info, lock)

    def find_node(self, id, rpc_id, socket=None, peer_id=None, peer_info=None, lock=None):
        message = {
            "message_type": "find_node",
            "id": id,
            "rpc_id": rpc_id
        }
        self.send_message(message, socket, peer_id, peer_info, lock)

    def found_nodes(self, id, nearest_nodes, rpc_id, socket=None, peer_id=None, peer_info=None, lock=None):
        message = {
            "message_type": "found_nodes",
            "id": id,
            "nearest_nodes": nearest_nodes,
            "rpc_id": rpc_id
        }
        self.send_message(message, socket, peer_id, peer_info, lock)

    def find_value(self, id, rpc_id, socket=None, peer_id=None, peer_info=None, lock=None):
        message = {
            "message_type": "find_value",
            "id": id,
            "rpc_id": rpc_id
        }
        self.send_message(message, socket, peer_id, peer_info, lock)

    def found_value(self, id, value, rpc_id, socket=None, peer_id=None, peer_info=None, lock=None):
        message = {
            "message_type": "found_value",
            "id": id,
            "value": value,
            "rpc_id": rpc_id
        }
        self.send_message(message, socket, peer_id, peer_info, lock)

    def astriple(self):
        return self.host, self.port, self.id, self.info

    def asquad(self):
        return self.host, self.port, self.id, self.info

    def address(self):
        return self.host, self.port

    def __repr__(self):
        return repr(self.astriple())

    def __str__(self):
        return "{0}:{1}".format(self.host, self.port)
