import time
import argparse
from ipaddress import IPv4Network
from dht import utils
from dht.dht import DHT

# constants

PORT = 9789

# setup arguments
parser = argparse.ArgumentParser()
parser.add_argument("--bootstrap", help="an established node to bootstrap from."
                                        " to specify a mother node, pass \"mother\"")
args = parser.parse_args()

print("Welcome to the little-bird demo")

# get details about the local network
ip, ip_format = utils.Utils.get_local_ip()

print("Your IP: {0} Range: {1}".format(ip, ip_format))

if not args.bootstrap:
    print("No bootstrap node specified, scanning")
    possible_hosts = []

    for host in IPv4Network(ip_format):
        possible_hosts.append(str(host))

    print("Scanning {} possible host(s)".format(len(possible_hosts)))

    hits = []

    for i, host in enumerate(possible_hosts):
        x = (i / len(possible_hosts)) * 100
        if utils.Utils.check_host_up(host, PORT):
            hits.append(host)
        print("\r{0}%".format(x), end=str())

    print("Done!")

    if len(hits) == 0:
        exit("No bootstrap nodes found")
    else:
        print(hits)
        host1, port1 = ip, PORT
        seeds = []
        for hit in hits:
            seeds.append((hit, PORT))
        dht1 = DHT(host1, port1, seeds=seeds)
elif args.bootstrap == "mother":
    print("Starting current instance as mother node")
    host1, port1 = ip, PORT
    dht1 = DHT(host1, port1)  # mother node
else:
    bootstrap = args.bootstrap
    bootstrap = bootstrap.split(":")
    if len(bootstrap) == 2:
        print("bootstrapping with {0}:{1}".format(bootstrap[0], bootstrap[1]))
        host1, port1 = ip, PORT
        dht1 = DHT(host1, port1, seeds=[(bootstrap[0], bootstrap[1])])
    else:
        exit("Invalid bootstrap node format. Use <host>:<port>")

while True:
    command = input("Enter a command")
    command = command.split(" ")
    if command[0] == "/exit":
        exit()
    elif command[0] == "/push":
        if len(command) != 3:
            print("Incorrect usage: /push <key> <value>")
        else:
            print("/push {0} {1}".format(command[1], command[2]))
            dht1[command[1]] = command[2]
    elif command[0] == "/pull":
        if len(command) == 2:
            print("/pull {0}".format(command[1]))
            try:
                print(dht1[command[1]])
                print("Pulled: {0}={1}".format(command[1], dht1[command[1]]))
            except KeyError:
                print("Key {0} not found.".format(command[1]))
        else:
            print("Incorrect usage: /pull <key>")
    else:
        print("Invalid command. Consult the documentation: <https://github.com/ZigmundVonZaun/little-bird>")

