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

    cell_response = (server.cell_status(cell_status))
    mobile_response = (server.mobile_status(mobile_status))

    print "\nGot command: \n"
    print cell_response['command']
    print '\nGot order: \n'
    if cell_response['order'] != 0:
        cell_status['state'] = 'STATE_WAIT'

    print cell_response['order']

    cell_response = (server.cell_status(cell_status))
    mobile_response = (server.mobile_status(mobile_status))

    print cell_response['order']

if __name__ == "__main__":
    main()


