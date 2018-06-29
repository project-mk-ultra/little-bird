import socket

from dht import utils

host = '192.168.0.1'
port = 80


print(utils.Utils.check_host_up(host, port))