#!/usr/bin/env python
__author__ = 'prier'

import xmlrpclib
import datetime
import time

server = xmlrpclib.ServerProxy('http://localhost:8000', use_datetime=True)
today = datetime.datetime.today()

cell_status = {
    'version_id': 1,
    'cell_id': 2,
    'state': 'STATE_FREE',
    'time': str(today),
    'status': "Human readable status message.."
}

mobile_status = {
    'version_id': 1,
    'robot_id': 3,
    'state': 'STATE_FREE',
    'time': str(today),
    'battery': 80,
    'position': "Station3",
    'status': "Human readable status message.."
}

done = False

def emulate_cell_robot(c_response):

    # Command state-machine for workcell

    print "Received Workcell command: " + c_response['command']

    if c_response['command'] == 'COMMAND_WAIT':
        cell_status['state'] = 'STATE_FREE'

    elif c_response['command'] == 'COMMAND_SORTBRICKS':
        cell_status['state'] = 'STATE_WORKING'

    elif c_response['command'] == 'COMMAND_LOADBRICKS':
        cell_status['state'] = 'STATE_WORKING'

    elif c_response['command'] == 'COMMAND_ABORT':
        cell_status['state'] = 'STATE_FREE'

    if cell_status['state'] == 'STATE_FREE':
        print "Workcell state is: 'STATE_FREE'"


def emulate_mobile_robot(m_response):
    global done

    # Command state-machine for mobile robot

    print "Received Mobile command: " + m_response['command']

    if m_response['command'] == 'COMMAND_WAIT':
        mobile_status['state'] = 'STATE_FREE'

    elif m_response['command'] == 'COMMAND_NAVIGATE':
        mobile_status['state'] = 'STATE_WORKING'

    elif m_response['command'] == 'COMMAND_TIP':
        mobile_status['state'] = 'STATE_WORKING'

    elif m_response['command'] == 'COMMAND_ABORT':
        mobile_status['state'] = 'STATE_FREE'


    # State-machine for the current mobile robot state
    if mobile_status['state'] == 'STATE_FREE':
        print "Mobile state is: 'STATE_FREE'"

    elif mobile_status['state'] == 'STATE_WORKING' and not done:
        print "Mobile state is: 'STATE_WORKING'"
        if m_response['command'] == 'COMMAND_TIP':
            # Tip of those bricks!
            print 'Tipping off bricks...'
            time.sleep(3)
            print 'The bricks are tipped off!'
        else:
            # Drive to next position
            time.sleep(2)
            print 'Position: ', m_response['path'], ' is reached!'
            mobile_status['position'] = m_response['path']
            done = True

    if done:
        print "Im am done, switching to STATE_FREE"
        mobile_status['state'] = 'STATE_FREE'
        done = False


def emulate_workcell():
    print 'Emulating workcell..'


def main():
    while True:
        print "Mobile state is: " + mobile_status['state']
        # Robot sends its status to MES-server every 2 seconds
        mobile_response = (server.mobile_status(mobile_status))
        emulate_mobile_robot(mobile_response)
        # Workcell sends its status to MES-server every 2 seconds
        print "Workcell state is: " + cell_status['state']
        workcell_response = (server.cell_status(cell_status))
        emulate_cell_robot(workcell_response)
        time.sleep(2)  # Delay for 2 seconds

if __name__ == "__main__":
    main()


