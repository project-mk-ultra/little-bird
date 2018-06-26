from dht.dht import DHT

host1, port1 = '0.0.0.0', 9789
dht1 = DHT(host1, port1)  # mother node
while True:
    command = input("Enter a command")
    command = command.split(" ")
    if command[0] == "/exit":
        exit()
    elif command[0] == "/push":
        if len(command) != 3:
            print("Incorrect usage: /push <key> <value>")
        else:
            print("/push {0}".format(command[1]))
            dht1["test"] = command[1]
    elif command[0] == "/pull":
        if len(command) == 2:
            print("/pull {0}".format(command[1]))
            print("Pulled: {0}={1}".format(command[1], dht1[command[1]]))
        else:
            print("Incorrect usage: /pull <key>")
    else:
        print("Invalid command. Consult the documentation: <https://github.com/ZigmundVonZaun/little-bird>")
