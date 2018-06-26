import time
from ipaddress import IPv4Network
from dht import utils

print("Welcome to the little-bird demo")

ip, ip_format = utils.Utils.get_local_ip()

print("Your IP: {0} LAN format: {1}".format(ip, ip_format))

possible_hosts = []

for host in IPv4Network(ip_format):
    possible_hosts.append(str(host))

print("Scanning {} possible host(s)".format(len(possible_hosts)))

hits = []

for i, host in enumerate(possible_hosts):
    x = (i / len(possible_hosts)) * 100
    utils.Utils.check_host_up(host, 9789)
    print("\r{0}%".format(x), end=str())

print("Done!")

if len(hits) == 0:
    exit("No boostrap nodes found")
