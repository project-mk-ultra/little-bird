### Little Bird Kademlia P2P DHT Network

[![Build Status](https://travis-ci.org/ZigmundVonZaun/little-bird.svg?branch=master)](https://travis-ci.org/ZigmundVonZaun/little-bird)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/) 

<img src="https://static.vecteezy.com/system/resources/previews/000/036/946/non_2x/oriole-bird-vector.jpg" width="320">

A Python3 Kademlia overlay network implementation.

### Introduction.

Kademlia is a pure P2P overlay network compromising also of a DHT (Distributed Hash Table).

The algorithm was proposed in the following paper:

https://pdos.csail.mit.edu/~petar/papers/maymounkov-kademlia-lncs.pdf

Often compared with the likes of Pastry and Chord, it is used in many projects in the networking
world including but not limited to BitTorrent, Ethereum, Gnutella, IPFS. 

### FAQ: Is this Kademlia implementation for you?

#### Is it anonymous?

No. Nodes use naked IP addresses to locate each other and share information 
within the network

#### Is the shared information encrypted?

No.Information is shared within the network without any encryption. However, adding an
encryption mechanism is trivial. 

This can be done by adding some logic to the `send_message()` logic and implementing a custom 
message received handler.

#### Does this implementation work on the public Internet?

Due to the complications of NAT punching, we decided to forego an implementation  that could work on the Internet. 

However, this remains in our future plans.


#### Is this also a database?

Yes. A distributed one with a very low failure rate. 
You can store and retrieve values at will.


 #### Why does it have a low failure rate?
 
 Keys are automatically replicated within different nodes in the network. Nodes that have a longer uptime
 are also favoured in this setup. 
 
 In fact the probability of failure is lower than the probability of a node leaving the
 network. The event of a node leaving the network does not affect the database in anyway.


#### Is there a central tracker server, like a master coordinator?

No. Every node shares the same weight in the network.
 
Each node holds substantial information which is useful in node and key lookups. 

Configuration information also spreads automatically as a side effect of key lookups.

Despite the lack of a tracker, all tracker functions are covered by Kademlia. 

Feature | Central Tracker Network | DHT Based Network
--- | --- | ---
Node Lookups  | [x] | [x] 
Key Lookups | [x] | [x]
Performance Increases With Load | [ ] | [x]
Susceptible to DDOS attacks | [x] | [ ]
Low failure rate | [ ] | [x]

#### Why do you keep on insisting that Kademlia is much more performant? Are you trying to sell it to me?

Because an increase in the number of nodes increases the performance of the network. 
Lookups are much faster. 

Whereas in the case of a centralised network, a tracker might be 
overwhelmed, taking down the whole network with it.

#### But wont the higher number of nodes effectively DDOS the network?

No. Kademlia favours older nodes over newer nodes.
 
A DDOS attack would just put the attacking nodes on the networks 
waiting list *chuckles villanously*

### Installation

### Demo

### Tests

    python -m unittest

### Behind the Scenes
