#!/usr/bin/env python
__author__ = 'prier'

import xmlrpclib
import datetime
import time
import random

server = xmlrpclib.ServerProxy('http://127.0.0.1:8000', use_datetime=True) #('http://192.168.1.50:8000', use_datetime=True)
today = datetime.datetime.today()

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
            time.sleep(1)
            print 'The bricks are tipped off!'
            done = True
        else:
            # Drive to next position
            time.sleep(1)
            print 'Position: ', m_response['path'], ' is reached!'
            mobile_status['position'] = m_response['path']
            done = True

    if done:
        print "Im am done, switching to STATE_FREE"
        mobile_status['state'] = 'STATE_FREE'
        done = False


def main():
    t_id = raw_input('Please choose an ID number for the client (1-3): ')
    mobile_status['robot_id'] = int(t_id)
    while True:
        print
        print "Mobile state is: " + mobile_status['state']
        # Robot sends its status to MES-server every 2 seconds
        #print server.print_state({'robot': 'Mobile3'})['response']
        mobile_response = (server.mobile_status(mobile_status))
        emulate_mobile_robot(mobile_response)
        print "Mobile state is: " + mobile_status['state']
        #print server.print_state({'robot': 'Mobile3'})['response']
        time.sleep(2)  # Delay for 2 seconds

if __name__ == "__main__":
    main()


