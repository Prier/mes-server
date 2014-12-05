#!/usr/bin/env python
__author__ = 'prier'

import xmlrpclib
import datetime
import time
import random

server = xmlrpclib.ServerProxy('http://127.0.0.1:8000', use_datetime=True) #('http://192.168.1.50:8000', use_datetime=True)
today = datetime.datetime.today()

cell_status = {
    'version_id': 1,
    'cell_id': 1,
    'state': 'STATE_FREE',
    'time': str(today),
    'status': "Human readable status message.."
}

done = False
sortingdone = 0
loadingdone = 0

def emulate_cell_robot(c_response):
    global sortingdone
    global loadingdone
    # Command state-machine for workcell

    print "Received Workcell command: " + c_response['command']

    if c_response['command'] == 'COMMAND_WAIT':
        if cell_status['state'] == 'STATE_OUTOFBRICKS':
            cell_status['state'] = 'STATE_OUTOFBRICKS'
        else:
            cell_status['state'] = 'STATE_FREE'

    elif c_response['command'] == 'COMMAND_SORTBRICKS':
        cell_status['state'] = 'STATE_SORTING'

    elif c_response['command'] == 'COMMAND_LOADBRICKS':
        cell_status['state'] = 'STATE_LOADING'

    elif c_response['command'] == 'COMMAND_ABORT':
        cell_status['state'] = 'STATE_FREE'

    if cell_status['state'] == 'STATE_FREE':
        print "Workcell state is: 'STATE_FREE'"

    elif cell_status['state'] == 'STATE_SORTING':
        print "Workcell state is: 'STATE_SORTING'"
        if sortingdone < 5:
            print "Sorting bricks..."
            sortingdone += 1
        else:
            print "Sorted bricks"
            sortingdone = 0
            #if random.randint(0, 10) < 5:

            cell_status['state'] = 'STATE_ORDERSORTED'

    elif cell_status['state'] == 'STATE_OUTOFBRICKS':
        print "Workcell state is: 'STATE_OUTOFBRICKS'"

    elif cell_status['state'] == 'STATE_LOADING':
        print "Workcell state is: 'STATE_LOADING'"
        print "Loading bricks onto Mobile robot..."
        time.sleep(3)
        if loadingdone < 3:
            loadingdone += 1
        else:
            loadingdone = 0
            cell_status['state'] = 'STATE_FREE'

    if cell_status['state'] == 'STATE_ORDERSORTED':
        print "Workcell state is: 'STATE_ORDERSORTED'"


def main():
    t_id = raw_input('Please choose an ID number for the client (1-3): ')
    cell_status['robot_id'] = int(t_id)
    while True:
        # Workcell sends its status to MES-server every 2 seconds
        print
        print "Workcell state is: " + cell_status['state']
        #print server.print_state({'robot': 'Cell1'})['response']
        workcell_response = (server.cell_status(cell_status))
        emulate_cell_robot(workcell_response)
        print "Workcell state is: " + cell_status['state']
        #print server.print_state({'robot': 'Cell1'})['response']
        resp = server.get_active_orders()
        print(resp)
        time.sleep(1)  # Delay for 2 seconds

if __name__ == "__main__":
    main()


