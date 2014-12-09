MES-server
==========

The awesome MES-server.

## Overview

The MES-server consists of Server.py and Resources.py. Running Server.py will start the server, which will listen for incoming connections from clients. The files ClientCell.py and ClientMobile.py are examples of how a client can connect to the server with XML-RPC, and can mainly be used as simulated workcells/mobile robots.

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

The first thing a client needs to know is the ip-address of the server. This is defined at the beginning of the client files. For testing you can have the server and client running on the same computer.

Secondly, they need to understand commands properly and know when and which status messages to send. The current client files pretend to do the work the server asks of them. The ROS node clients from the rsd\_mes\_client repository should be used for the actual project.

So: The client connects to the server, and then periodically sends a status message via a XML-RPC call. This means they will get a response back with a command, which will tell them what to do. How this works in detail for each platform is detailed below.

### The Mobile Client

The state machine of the mobile robot (from the viewpoint of the server) should be as seen in the image below:

![ddgh](http://i.imgur.com/XdXQzcP.png "State machine for mobile robot")

This means that the robot should start in STATE\_FREE, and periodically tell the server its state. At some point there will be something for the robot to do, and it will return a command other than COMMAND\_WAIT. The robot should start doing that (e.g. move to a new area), and when its state changes (e.g. it arrives at the area and is free again, or it finishes tipping bricks off), it should again update the server with its state. If the robot is told to wait, it should periodically tell the server its state again, so the server can give it a new job when something comes up.

Below are quick references for the ROS messages needed.

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

The command format for the mobile robot is:

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

The state machine of the workcell robot (from the viewpoint of the server) should be as seen in the image below:

![ddgh](http://i.imgur.com/Anqak4s.png "State machine for workcell robot")

[Explanation of workcell robot behaviour].

Below are quick references for the ROS messages needed.

The status message for the cell robots is as follows:

```
Header header

uint8 version_id  # Version of the client

uint8 robot_id    # Robot id

uint8 STATE_FREE=0
uint8 STATE_SORTING=1
uint8 STATE_OUTOFBRICKS=2
uint8 STATE_ORDERSORTED=3
uint8 STATE_LOADING=4
uint8 state       # When the platform is done loading, the state should be considered free.

uint8 done_pct    # For future use. Return 0 when not working

string status     # Feel free to use this to write a human readable status of the robot. This may show up on the MES dashboard.
```

The command format for the cell robot is:

```
Header header

uint8 COMMAND_WAIT = 0
uint8 COMMAND_SORTBRICKS = 1
uint8 COMMAND_LOADBRICKS = 2
uint8 COMMAND_ABORT = 3
uint8 command    # The command that should be started by the robot

mes_order order  # This is further defined below
```

The mes_order message is:

```
uint16 order_id
lego_brick[] bricks
```

And a lego_brick is:

```
uint8 COLOR_RED = 0
uint8 COLOR_BLUE = 1
uint8 COLOR_YELLOW = 2
uint8 color
uint8 count
```

### Extra area info

There are some marks with coordinates on the floor in robolab, which should fit together with the coordinates returned by the camera locator. Going by these coordinates, we have defined the various areas as rectangles. Below is a list of the areas along with the lower left and upper right corner (the loadoff1 and loadon1 are very approximate):

```
FloorOut,  -2.00,-2.15,   -0.15, 1.00,
FloorIn,   -0.15,-2.15,    2.50, 1.00,
RampOut,   -1.00,-4.70,   -0.15,-2.15,
RampIn,    -0.15,-4.10,    0.40,-2.15,
InBox,     -0.15,-5.80,    0.35,-4.10,
Dispenser, -1.00,-5.80,   -0.15,-4.70,
Station1,   0.35,-4.65,    1.15,-4.10,
Station2,   0.35,-5.20,    1.15,-4.65,
Station3,   0.35,-5.80,    1.15,-5.20,
LineLeft,  -4.00, 0.00,   -2.00, 1.95,
LineMid,   -2.00, 1.00,    2.50, 1.95,
LineRight,  2.50, 0.00,    5.50, 1.95,
LoadOff1,   3.40, 1.95,    4.00, 3.00,
LoadOn1,    4.00, 1.95,    4.60, 3.00,
LoadOff2,   0.75, 1.95,    1.35, 3.00,
LoadOn2,    1.35, 1.95,    1.95, 3.00,
LoadOff3,  -2.20, 1.95,   -1.60, 3.00,
LoadOn3,   -1.60, 1.95,   -1.00, 3.00
```
