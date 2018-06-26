import hashlib
import netifaces
import random
import socket

id_bits = 128


class Utils:
    @staticmethod
    def largest_differing_bit(value1, value2):
        distance = value1 ^ value2
        length = -1
        while distance:
            distance >>= 1
            length += 1
        return max(0, length)

    @staticmethod
    def hash_function(data, algo='sha256'):
        if algo == 'md5':
            return int(hashlib.md5(data.encode('ascii')).hexdigest(), 16)
        if algo == 'sha256':
            return int(hashlib.sha256(data.encode('utf8')).hexdigest(), 16)

    @staticmethod
    def random_id(seed=None):
        if seed:
            random.seed(seed)
        return random.randint(0, (2 ** id_bits) - 1)

    @staticmethod
    def get_local_ip():
        interfaces = netifaces.interfaces()

        for interface in interfaces:
            addrs = netifaces.ifaddresses(interface)
            try:
                ip = addrs[netifaces.AF_INET][0]['addr']
                octets = ip.split(".")
                if octets[0] == '192':
                    ip_format = "{0}.{1}.{2}.0/24".format(octets[0], octets[1], octets[2])
                    return ip, ip_format
            except KeyError as e:
                print("No 192.168.0.0/24 or 192.168.1.0/24 address found for interface {0}".format(interface))
        exit("Could not find a valid 192.168.0.0/24 or 192.168.1.0/24 interface")

    @staticmethod
    def check_host_up(host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        if result == 0:
            return True
        else:
            return False

