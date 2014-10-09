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

active_orders = []


class Order():
    def __init__(self, order, robot):
        self.order = order
        self.allocatedArea = []
        self.allocatedRobot = robot
        self.status = 'unstarted'


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
            if next_order != 0:
                new_order = Order(next_order, robot_name)
                command = resource_handler.get_command(new_order, robot_name, m_status)
                if command != 0:

                    new_order.status = 'to_dispenser'
                else:



                mobile_response = {

                }
                print 'there are orders'
            else:
                print 'No orders'

    # Save state information
    if m_status['state'] == 'STATE_FREE':
        free_robot = {
            'robot_id': m_status['robot_id'],
            'time': m_status['time']
        }
        free_robot_list.append(free_robot)

    # Response

    mobile_response = {

    }


def cell_status(c_status):
    for k, v in c_status.items():
        print k, ' = ', v

    resp_order = 0
    resp_cmd = ''

    # Save state information
    if c_status['state'] == 'STATE_FREE':
        free_cell = {
            'cell_id': c_status['cell_id'],
            'time': c_status['time']
        }
        free_cell_list.append(free_cell)

    if free_cell_list and free_robot_list:
        if c_status['cell_id'] == free_cell_list[0]['cell_id']:
            resp_cmd = 'COMMAND_WAIT'
            resp_order = fetch_order()
            free_cell_list.popleft()
            free_robot_list.popleft()
        else:
            resp_order = 0

    # Response
    cell_response = {
        'command': resp_cmd,
        'order': resp_order,
    }

    return cell_response


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
