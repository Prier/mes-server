MES-server
==========

The awesome MES-server.

## Overview

The MES-server consists of Server.py and Resources.py. Running Server.py will start the server, which will listen for incoming connections from clients. The files ClientCell.py and ClientMobile.py are examples of how a client can connect to the server with XML-RPC.

#### Areas:
* Dispenser
* Station1
* Station2
* Station3
* RampOut
* RampIn
* FloorOut
* FloorIn
* Line
* LoadOff1
* LoadOn1
* LoadOff2
* LoadOn2
* LoadOff3
* LoadOn3

## Info for clients

The first thing a client needs to know is the ip-address of the server. This is defined at the beginning of the client files. For testing you can have the server and client running on the same computer, in which case the ip will already fit; otherwise always remember to change it.

Secondly, they need to understand commands properly and know when and what to status messages to send. The current client files pretend to do the work the server asks of them, and are examples of how the communication works.

### The Mobile Client

