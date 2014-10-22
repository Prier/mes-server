MES-server
==========

The awesome MES-server.

## Overview

The MES-server consists of Server.py and Resources.py. Running Server.py will start the server, which will listen for incoming connections from clients. The files ClientCell.py and ClientMobile.py are examples of how a client can connect to the server with XML-RPC.

#### Areas:
* Dispenser
* InBox
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

![test](http://i.imgur.com/x0nrDWh.png?1 "Floor plan")

## Info for clients

The first thing a client needs to know is the ip-address of the server. This is defined at the beginning of the client files. For testing you can have the server and client running on the same computer, in which case the ip will already fit; otherwise always remember to change it.

Secondly, they need to understand commands properly and know when and which status messages to send. The current client files pretend to do the work the server asks of them, and are examples of how the communication works.

So: The client connects to the server, and then periodically sends a status message via a XML-RPC call. This means they will get a response back with a command, which will tell them what to do. How this works in detail for each platform is detailed below.

### The Mobile Client

![ddgh](http://i.imgur.com/XdXQzcP.png "Text")


The status message for the mobile robots is as follows:

```
Header header

uint8 version_id  # Version of the client

uint8 robot_id    # Robot id

uint8 STATE_FREE=0
uint8 STATE_ERROR=1
uint8 STATE_WORKING=2
uint8 state       # When the robot has completed a task it shall return STATE_FREE

uint8 done_pct    # For future use. Return 0 when not working

uint16 battery    # This is the raw value from the frobomind controller taken directly from the ADC

string position   # The position of the mobile platform

string status     # Feel free to use this to write a human readable status of the robot. This may show up on the MES dashboard.
```

The command:

```
Header header

uint8 COMMAND_WAIT = 0
uint8 COMMAND_NAVIGATE = 1
uint8 COMMAND_TIP = 2
uint8 COMMAND_ABORT = 3
uint8 command   # The command that should be started by the robot

string path     # If the command is COMMAND_NAVIGATE, this will be the next destination of the robot, in the form of one of the strings above
```

### The Cell Client

![ddgh](http://i.imgur.com/Anqak4s.png "Text")
