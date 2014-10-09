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
    'position': 'Parking',
    'status': "Human readable status message.."
}


def main():

    modified_cell_status = cell_status
    modified_cell_status['state'] = 'STATE_SORTING'

    modified2_cell_status = cell_status
    modified2_cell_status['state'] = 'STATE_OUTOFBRICKS'

    modified3_cell_status = mobile_status
    modified3_cell_status['state'] = 'STATE_ORDERSORTED'

    modified4_cell_status = mobile_status
    modified4_cell_status['state'] = 'STATE_LOADING'

    modified_mobile_status = cell_status
    modified_mobile_status['state'] = 'STATE_ERROR'

    modified2_mobile_status = cell_status
    modified2_mobile_status['state'] = 'STATE_WORKING'

    cell_response = (server.cell_status(cell_status))
    mobile_response = (server.mobile_status(mobile_status))

    print "\nGot command: \n"
    print cell_response['command']
    print '\nGot order: \n'
    if cell_response['order'] != 0:
        cell_status['state'] = 'STATE_WAIT'

    if mobile_response['order'] != 0:
        mobile_status['state'] = 'STATE_WAIT'

    print cell_response['order']

    cell_response = (server.cell_status(cell_status))
    mobile_response = (server.mobile_status(mobile_status))

    print cell_response['order']
    print mobile_response['order']

    cell_response = (server.cell_status(modified_cell_status))
    mobile_response = (server.mobile_status(modified_mobile_status))

    print "\nGot command: \n"
    print cell_response['command']
    print '\nGot order: \n'
    if cell_response['order'] != 0:
        cell_status['state'] = 'STATE_WAIT'

    if mobile_response['order'] != 0:
        mobile_status['state'] = 'STATE_WAIT'

    print cell_response['order']

    cell_response = (server.cell_status(cell_status))
    mobile_response = (server.mobile_status(mobile_status))

    print cell_response['order']
    print mobile_response['order']

    cell_response = (server.cell_status(modified2_cell_status))
    mobile_response = (server.mobile_status(modified2_mobile_status))

    print "\nGot command: \n"
    print cell_response['command']
    print '\nGot order: \n'
    if cell_response['order'] != 0:
        cell_status['state'] = 'STATE_WAIT'

    if mobile_response['order'] != 0:
        mobile_status['state'] = 'STATE_WAIT'

    print cell_response['order']

    cell_response = (server.cell_status(cell_status))
    mobile_response = (server.mobile_status(mobile_status))

    print cell_response['order']
    print mobile_response['order']

    cell_response = (server.cell_status(modified3_cell_status))
    mobile_response = (server.mobile_status(modified2_mobile_status))

    print "\nGot command: \n"
    print cell_response['command']
    print '\nGot order: \n'
    if cell_response['order'] != 0:
        cell_status['state'] = 'STATE_WAIT'

    if mobile_response['order'] != 0:
        mobile_status['state'] = 'STATE_WAIT'

    print cell_response['order']

    cell_response = (server.cell_status(cell_status))
    mobile_response = (server.mobile_status(mobile_status))

    print cell_response['order']
    print mobile_response['order']

    cell_response = (server.cell_status(modified4_cell_status))
    mobile_response = (server.mobile_status(modified2_mobile_status))

    print "\nGot command: \n"
    print cell_response['command']
    print '\nGot order: \n'
    if cell_response['order'] != 0:
        cell_status['state'] = 'STATE_WAIT'

    if mobile_response['order'] != 0:
        mobile_status['state'] = 'STATE_WAIT'

    print cell_response['order']

    cell_response = (server.cell_status(cell_status))
    mobile_response = (server.mobile_status(mobile_status))

    print cell_response['order']
    print mobile_response['order']

if __name__ == "__main__":
    main()


