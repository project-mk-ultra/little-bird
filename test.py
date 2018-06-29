import socket

from dht import utils

host = '192.168.0.66'
port = 9789


print(utils.Utils.check_host_up(host, port))