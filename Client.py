#!/usr/bin/env python
__author__ = 'prier'

import xmlrpclib
import datetime

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
    'position': "Floor",
    'status': "Human readable status message.."
}

def emulate_mobile_robot(m_response):
    print 'Emulating mobile robot..'

    # Test state-machine for mobile robot
    if m_response['command'] == 'COMMAND_WAIT':
        mobile_status['state'] = 'STATE_FREE'
        print

    print mobile_response

    if mobile_response['command'] == 'COMMAND_WAIT':
        mobile_status['state'] = 'STATE_WAIT'

    print mobile_response

def emulate_workcell():
    print 'Emulating workcell..'


def main():
    while 1:
        # Robot sends its status to MES-server
        mobile_response = (server.mobile_status(mobile_status))
        emulate_mobile_robot(mobile_response)

if __name__ == "__main__":
    main()


