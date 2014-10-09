#!/usr/bin/env python
__author__ = 'prier'

import argparse
import threading
import random
import datetime
from twisted.internet import task
from twisted.internet import reactor
import Queue
from collections import deque
from SimpleXMLRPCServer import SimpleXMLRPCServer
import Resources

# The resource handler

resource_handler = Resources.ResourceHandler()

# MES variables

order_id = 0
order_queue = Queue.Queue()
free_robot_list = deque([])
free_cell_list = deque([])

# MES functions

def generate_order():
    # generate order
    global order_id
    order_id += 1
    order = {
        'order_id': order_id,
        'bricks':
            dict(color_red=random.randint(3, 8), color_blue=random.randint(3, 8), color_yellow=random.randint(3, 8)),
        'time': str(datetime.datetime.today())
    }
    order_queue.put(order)


def fetch_order():
    if not order_queue.empty():
        return order_queue.get()
    else:
        return 0


def mobile_status(m_status):
    for k, v in m_status.items():
        print k, ' = ', v

    robot_id = m_status['robot_id']
    robot_name = resource_handler.get_mobile_robot_name(robot_id)
    order = resource_handler.get_mobile_robot(robot_id).boundToOrder
    if order != 0:
        print 'nanananaananananabaatmaan'
    else:
        if m_status['state'] == 'STATE_FREE':
            next_order = fetch_order()
            command = 0

            if next_order != 0:
                command = resource_handler.get_command_m(next_order, robot_name, m_status)

            if command == 0:
                command = {
                    'command': 'COMMAND_WAIT'
                }
            return command
        elif m_status['state'] == 'STATE_WORKING':
            command = resource_handler.get_command_m(robot_name, m_status)
            return command
        elif m_status['state'] == 'STATE_ERROR':
            return dict(command='COMMAND_ABORT')
        else:
            return dict(command='COMMAND_ABORT')



def cell_status(c_status):
    for k, v in c_status.items():
        print k, ' = ', v

    # Save state information
    if order != 0:
        print 'nanananaananananabaatmaan'
    else:
        if c_status['state'] == 'STATE_FREE':
            next_order = fetch_order()
            command = 0

            if next_order != 0:
                command = resource_handler.get_command_c(next_order, robot_name, c_status)

            if command == 0:
                command = {
                    'command': 'COMMAND_WAIT'
                }
            return command
        elif c_status['state'] == 'STATE_SORTING':
            command = resource_handler.get_command_c(robot_name, c_status)
            return command
        elif c_status['state'] == 'STATE_OUTOFBRICKS':
            return dict(command='COMMAND_WAIT')
        elif c_status['state'] == 'STATE_ORDERSORTED':
            return dict(command='STATE_WAIT')
        elif c_status['state'] == 'STATE_LOADING':
            return dict(command='COMMAND_SORTBRICKS')
        elif c_status['state'] == 'STATE_ERROR':
            return dict(command='COMMAND_ABORT')
        else:
            return dict(command='COMMAND_ABORT')


class ServerThread(threading.Thread):
    def __init__(self, server_addr):
        threading.Thread.__init__(self)
        self.server = SimpleXMLRPCServer(server_addr, logRequests=True, allow_none=True)
        self.server.register_multicall_functions()
        self.server.register_function(cell_status, 'cell_status')
        self.server.register_function(mobile_status, 'mobile_status')

    def run(self):
        self.server.serve_forever()


def run_server(host, port):
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
    l = task.LoopingCall(generate_order)
    l.start(10.0)  # call every second

    # l.stop() will stop the looping calls
    reactor.run()


if __name__ == "__main__":
    main()
