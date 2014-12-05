__author__ = 'kristjan'

import argparse
import time
import xmlrpclib
import threading
import random
from SimpleXMLRPCServer import SimpleXMLRPCServer

server = xmlrpclib.ServerProxy('http://192.168.1.50:8000', use_datetime=True)

seconds_to_remain_open = 5


def open_dispenser():
    #insert dispenser opening logic here
    return 0


def close_dispenser():
    #insert dispenser closing logic here
    return 0


class DispenserThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.id = random.randint(0, 1000)

    def run(self):
        print("Dispenser thread #" + self.id + ": Opening dispenser")
        open_dispenser()
        time.sleep(seconds_to_remain_open)
        print("Dispenser thread #" + self.id + ": Closing dispenser")
        close_dispenser()
        print("Dispenser thread #" + self.id + ": Informing server about finished dispensing")
        server.finished_dispensing()
        print("Dispenser thread #" + self.id + ": Ending dispenser thread")


def dispense():
    print("Starting dispenser")
    dispenser_thread = DispenserThread()
    dispenser_thread.start()
    print("Returning from rpc")


class ServerThread(threading.Thread):
    def __init__(self, server_addr):
        threading.Thread.__init__(self)
        self.server = SimpleXMLRPCServer(server_addr, logRequests=True, allow_none=True)
        self.server.register_multicall_functions()
        self.server.register_function(dispense, 'dispense')

    def run(self):
        self.server.serve_forever()


def main():
    connected = False

    parser = argparse.ArgumentParser(description='Multithreaded MES XMLRPC Dispenser Software')
    parser.add_argument('--host', action="store", dest="host", default='localhost')
    parser.add_argument('--port', action="store", dest="port", default=8001, type=int)

    # parse arguments
    given_args = parser.parse_args()
    host, port = given_args.host, given_args.port
    local_server = ServerThread((host, port))
    local_server.start()

    while True:
        if not connected:
            print("Trying connection ... ")
            try:
                server.register_dispenser(0)
                connected = True
                print("Connected to server.")
            except:
                connected = False
                print("No connection to server.")
        time.sleep(5)


if __name__ == "__main__":
    main()