#!/usr/bin/env python
__author__ = 'armienn & reaver'

import argparse
import threading
import random
import datetime
from twisted.internet import task
from twisted.internet import reactor
from collections import deque
from SimpleXMLRPCServer import SimpleXMLRPCServer
import xmlrpclib
import Resources

start_up_time = datetime.datetime.today()

log_name = "log " + str(start_up_time.date()) + " " + str(start_up_time.hour) + "-" + str(start_up_time.minute) + '.txt'
last_log = datetime.datetime.today()
log = ""
finished_orders = 0

# The resource handler

resource_handler = Resources.ResourceHandler()

# MES variables

order_id = 0
order_queue = deque([])
free_robot_list = deque([])
free_cell_list = deque([])

dispenser = {'ip': 'http://127.0.0.1:8001',
             'connected': False,
             'connection': None}

# MES functions


def generate_order():
    # generate order
    bricks = [
        dict(color='COLOR_RED', size=6, count=random.randint(0, 8)),
        dict(color='COLOR_BLUE', size=6, count=random.randint(0, 8)),
        dict(color='COLOR_YELLOW', size=6, count=random.randint(0, 8))]
    add_order(bricks)


def add_order(bricks):
    global order_id
    order_id += 1
    order = {
        'order_id': order_id,
        'bricks': bricks
    }
    order_queue.append(order)
    print("Added order: " + str(order))
    log_write(str(datetime.datetime.today()) + '\n')
    log_write("  Added order: " + str(order) + '\n')


def print_state(robot_status):
    return resource_handler.print_state(robot_status['robot'])


def mobile_status(m_status):
    log_write(str(datetime.datetime.today()) + '\n')
    log_write("  Message from mobile:\n")
    for k, v in m_status.items():
        print k, ' = ', v
        log_write("    " + str(k) + " = " + str(v) + '\n')

    robot_id = m_status['robot_id']
    resource_handler.get_mobile_robot(robot_id).alive = True
    robot_name = Resources.get_mobile_robot_name(robot_id)
    order = resource_handler.get_mobile_robot(robot_id).bound_to_order
    if order != 0:
        print robot_name, ' is working on order #', resource_handler.resources[robot_name].bound_to_order.order['order_id']

        if m_status['state'] == 'STATE_FREE' or m_status['state'] == 'STATE_WORKING':
            command = resource_handler.get_command_m(robot_name, m_status, dispenser, finish_order)

            if command == 0:
                command = {
                    'command': 'COMMAND_WAIT'
                }
                print robot_name, ' is waiting\n'
            print robot_name, ' got: '+command['command']+'\n'

        elif m_status['state'] == 'STATE_ERROR':
            command = dict(command='COMMAND_ABORT')

        else:
            command = dict(command='COMMAND_ABORT')
    else:
        if m_status['state'] == 'STATE_FREE':
            print robot_name, ' is available\n'

            new_order = resource_handler.get_order(robot_name, m_status, order_queue)
            print new_order
            if new_order != 0:
                print ' ', new_order.status, ' ', new_order.allocated_cell, ' ', new_order.allocated_robot
            command = 0
            if new_order != 0:
                command = resource_handler.get_command_m(robot_name, m_status, dispenser)
                print command

            if command == 0:
                command = {
                    'command': 'COMMAND_WAIT'
                }
            print robot_name, ' is waiting\n'

        elif m_status['state'] == 'STATE_WORKING':  # This shouldn't happen
            print robot_name, ' is working\n'
            command = dict(command='COMMAND_ABORT')

        elif m_status['state'] == 'STATE_ERROR':
            print robot_name, ' has encountered an error! ABORTING...\n'
            command = dict(command='COMMAND_ABORT')

        else:
            print robot_name, ': Error in states! ABORTING...\n'
            command = dict(command='COMMAND_ABORT')

    log_write("  Returning command:\n")
    for k, v in command.items():
        log_write("    " + str(k) + " = " + str(v) + '\n')
    return command


def cell_status(c_status):
    log_write(str(datetime.datetime.today()) + '\n')
    log_write("  Message from cell:\n")
    for k, v in c_status.items():
        print k, ' = ', v
        log_write("    " + str(k) + " = " + str(v) + '\n')

    # Save state information
    cell_id = c_status['robot_id']
    resource_handler.get_cell_robot(cell_id).alive = True
    robot_name = Resources.get_cell_robot_name(cell_id)
    order = resource_handler.get_cell_robot(cell_id).bound_to_order
    if order != 0:
        print robot_name, ' is working on order #', order.order['order_id']
        if c_status['state'] == 'STATE_FREE':
            command = resource_handler.get_command_c_free(robot_name, c_status)

            if command == 0:
                command = {
                    'command': 'COMMAND_WAIT'
                }
                print robot_name, ' is waiting\n'

        elif c_status['state'] == 'STATE_SORTING':
            print robot_name, ' is sorting\n'
            command = resource_handler.get_command_c_sorting(robot_name)
            if command == 0:
                command = {
                    'command': 'COMMAND_WAIT'
                }
                print robot_name, ' is waiting\n'

        elif c_status['state'] == 'STATE_ORDERSORTED':
            print robot_name, ' is done sorting\n'
            command = resource_handler.get_command_c_done_sorting(robot_name)
            if command == 0:
                command = {
                    'command': 'COMMAND_WAIT'
                }
                print robot_name, ' is waiting\n'

        elif c_status['state'] == 'STATE_OUTOFBRICKS':
            print robot_name, ' is out of bricks\n'
            command = resource_handler.get_command_c_out_of_bricks(robot_name)
            if command == 0:
                command = {
                    'command': 'COMMAND_WAIT'
                }
                print robot_name, ' is waiting\n'

        elif c_status['state'] == 'STATE_LOADING':
            print robot_name, ' is loading bricks\n'
            command = resource_handler.get_command_c_loading_bricks(robot_name)
            if command == 0:
                command = {
                    'command': 'COMMAND_WAIT'
                }
                print robot_name, ' is waiting\n'

        elif c_status['state'] == 'STATE_ERROR':
            print robot_name, ' has encountered an error! ABORTING...\n'
            command = dict(command='COMMAND_ABORT')

        else:
            print robot_name, ': Error in states! ABORTING...\n'
            command = dict(command='COMMAND_ABORT')
    else:
        if c_status['state'] == 'STATE_FREE':

            command = {
                'command': 'COMMAND_WAIT'
            }
            print robot_name, ' is waiting\n'

        elif c_status['state'] == 'STATE_ORDERSORTED':  # shouldn't happen
            print robot_name, ': Error in states! ABORTING...\n'
            command = dict(command='COMMAND_ABORT')

        elif c_status['state'] == 'STATE_LOADING':  # shouldn't happen
            print robot_name, ': Error in states! ABORTING...\n'
            command = dict(command='COMMAND_ABORT')

        elif c_status['state'] == 'STATE_ERROR':
            print robot_name, ' has encountered an error! ABORTING...\n'
            command = dict(command='COMMAND_ABORT')

        else:
            print robot_name, ': Error in states! ABORTING...\n'
            command = dict(command='COMMAND_ABORT')

    log_write("  Returning command:\n")
    for k, v in command.items():
        log_write("    " + str(k) + " = " + str(v) + '\n')
    return command


def log_write(text):
    global log, last_log
    log += text
    if (datetime.datetime.today() - last_log) > datetime.timedelta(seconds=10):
        last_log = datetime.datetime.today()
        f = open(log_name, 'a')
        f.write(log)
        f.close()
        log = ""


def get_log():
    global log, last_log
    last_log = datetime.datetime.today()
    f = open(log_name, 'a')
    f.write(log)
    f.close()
    local_log = log
    log = ""
    return local_log


def get_status():
    value = {}
    status = {'order': resource_handler.resources['Cell1'].bound_to_order,
              'taken': resource_handler.resources['Cell1'].taken,
              'alive': resource_handler.resources['Cell1'].alive}
    value['Cell1'] = status.copy()

    status = {'order': resource_handler.resources['Cell2'].bound_to_order,
              'taken': resource_handler.resources['Cell2'].taken,
              'alive': resource_handler.resources['Cell2'].alive}
    value['Cell2'] = status.copy()

    status = {'order': resource_handler.resources['Cell3'].bound_to_order,
              'taken': resource_handler.resources['Cell3'].taken,
              'alive': resource_handler.resources['Cell3'].alive}
    value['Cell3'] = status.copy()

    status = {'order': resource_handler.resources['Mobile1'].bound_to_order,
              'taken': resource_handler.resources['Mobile1'].taken,
              'alive': resource_handler.resources['Mobile1'].alive}
    value['Mobile1'] = status.copy()

    status = {'order': resource_handler.resources['Mobile2'].bound_to_order,
              'taken': resource_handler.resources['Mobile2'].taken,
              'alive': resource_handler.resources['Mobile2'].alive}
    value['Mobile2'] = status.copy()

    status = {'order': resource_handler.resources['Mobile3'].bound_to_order,
              'taken': resource_handler.resources['Mobile3'].taken,
              'alive': resource_handler.resources['Mobile3'].alive}
    value['Mobile3'] = status.copy()

    print(str(value))
    return value


def get_inactive_orders():
    value = []
    for thing in order_queue:
        value.append(thing)
    return value


def get_active_orders():
    cell1order = resource_handler.resources['Cell1'].bound_to_order
    cell2order = resource_handler.resources['Cell2'].bound_to_order
    cell3order = resource_handler.resources['Cell3'].bound_to_order

    value = []

    if cell1order != 0:
        value.append(cell1order.order)
    if cell2order != 0:
        value.append(cell2order.order)
    if cell3order != 0:
        value.append(cell3order.order)
    return value


def get_OEE_data():
    data = {}
    delta = datetime.datetime.today() - start_up_time
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    data['uptime'] = "Days: " + str(delta.days) + " H:M:S: " + str(hours) + ":" + str(minutes) + ":" + str(seconds)
    data['orders_waiting'] = len(order_queue)
    data['orders_processed'] = finished_orders
    return data


def finish_order(order):
    log_write(str(datetime.datetime.today()) + '\n')
    log_write("  Finished order:\n")
    log_write("    " + str(order))
    global finished_orders
    finished_orders += 1


def register_dispenser(ip):
    #dispenser['ip'] = ip
    dispenser['connection'] = xmlrpclib.ServerProxy(dispenser['ip'], use_datetime=True)
    dispenser['connected'] = True
    print("Dispenser registered")


def finished_dispensing():
    resource_handler.dispenser_has_dispensed = True
    print("Dispenser has dispensed")


class ServerThread(threading.Thread):
    def __init__(self, server_addr):
        threading.Thread.__init__(self)
        self.server = SimpleXMLRPCServer(server_addr, logRequests=True, allow_none=True)
        self.server.register_multicall_functions()
        self.server.register_function(register_dispenser, 'register_dispenser')
        self.server.register_function(finished_dispensing, 'finished_dispensing')
        self.server.register_function(cell_status, 'cell_status')
        self.server.register_function(mobile_status, 'mobile_status')
        self.server.register_function(print_state, 'print_state')
        self.server.register_function(get_inactive_orders, 'get_inactive_orders')
        self.server.register_function(get_active_orders, 'get_active_orders')
        self.server.register_function(add_order, 'add_order')
        self.server.register_function(get_status, 'get_status')
        self.server.register_function(get_log, 'get_log')
        self.server.register_function(get_OEE_data, 'get_OEE_data')

    def run(self):
        self.server.serve_forever()


def run_server(host, port):
    f = open(log_name, 'w')
    f.write('MES starting with host as ' + str(host) + ' and port ' + str(port) + '\n')
    f.close()
    # server code
    server_addr = (host, port)
    server = ServerThread(server_addr)
    server.start()  # The server is now running
    print '\n####### MES-server 2014 #######\n'
    print "Server thread started. Testing the server..."


def main():
    parser = argparse.ArgumentParser(description='Multithreaded MES XMLRPC Server')
    parser.add_argument('--host', action="store", dest="host", default='localhost')
    parser.add_argument('--port', action="store", dest="port", default=8000, type=int)
    # parse arguments
    given_args = parser.parse_args()
    host, port = given_args.host, given_args.port
    run_server(host, port)

    # generate order
    #l = task.LoopingCall(generate_order)
    #l.start(10.0)  # call every ten seconds

    # l.stop() will stop the looping calls
    #reactor.run()


if __name__ == "__main__":
    main()
