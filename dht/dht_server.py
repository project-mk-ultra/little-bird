import socketserver
import threading


class DHTServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    def __init__(self, host_address, handler_cls):
        """
        Initialises a UDP socket server needed in order to receive communications from other nodes in the network.
        :param host_address: Host address.
        :param handler_cls: Specify handler that fires after a message is received.
        """
        socketserver.UDPServer.__init__(self, host_address, handler_cls)
        self.send_lock = threading.Lock()
