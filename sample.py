import matplotlib.pyplot as plt
import networkx as nx

from dht.dht import DHT

G = nx.Graph()  # network graph

host1, port1 = 'localhost', 9789
dht1 = DHT(host1, port1)  # mother node
G.add_node(str(dht1.peer))
host2, port2 = 'localhost', 9788
dht2 = DHT(host2, port2, seeds=[(host1, port1)])  # bootstrap into network using mother node
G.add_node(str(dht2.peer))
dht1["my_key"] = ["foo", "bar", "fizz", "buzz"]

for i in range(10):
    host, port = "localhost", 9787 - i
    dht3 = DHT(host, port, seeds=[(host1, port1)])
    print(dht3.buckets.to_list())
    G.add_node(str(dht3.peer))
    # G.add_edge(str(dht3.peer), "localhost:{0}".format(9787-i+1))

# G.add_edge("localhost:{0}".format(9778), "localhost:{0}".format(9789))
# G.add_edge("localhost:{0}".format(9789), "localhost:{0}".format(9788))

print(dht2["my_key"])  # blocking get
dht2.get("my_key", lambda data: print(data))  # threaded get


nx.draw(G, with_labels=True, font_weight='bold')

plt.show()
