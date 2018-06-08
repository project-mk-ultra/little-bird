### Little Bird Kademlia P2P DHT Network

[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/) 

<img src="https://static.vecteezy.com/system/resources/previews/000/036/946/non_2x/oriole-bird-vector.jpg" width="320">

A Python3 Kademlia overlay network implementation.

### Introduction.

Kademlia is a pure P2P overlay network compromising also of a DHT (Distributed Hash Table).

The algorithm was proposed in the following paper:

https://pdos.csail.mit.edu/~petar/papers/maymounkov-kademlia-lncs.pdf

Often compared with the likes of Pastry and Chord, it is used in many projects in the networking
world including but not limited to Bittorent, Ethereum, Gnutella, IPFS. 

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

### Installation

### Demo

### Tests

    python -m unittest

### Behind the Scenes
