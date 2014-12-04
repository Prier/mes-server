__author__ = 'kristjan'

import argparse
import time
import xmlrpclib
import threading
#from twisted.internet import reactor
from SimpleXMLRPCServer import SimpleXMLRPCServer

server = xmlrpclib.ServerProxy('http://192.168.1.50:8000', use_datetime=True)

seconds_to_remain_open = 5


def open_dispenser():
    #insert dispenser opening logic here
    return 0


def close_dispenser():
    #insert dispenser closing logic here
    return 0


def dispense():
    open_dispenser()
    time.sleep(seconds_to_remain_open)
    close_dispenser()
    server.finished_dispensing()


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

    parser = argparse.ArgumentParser(description='Multithreaded MES XMLRPC Server')
    parser.add_argument('--host', action="store", dest="host", default='localhost')
    parser.add_argument('--port', action="store", dest="port", default=8000, type=int)

    # parse arguments
    given_args = parser.parse_args()
    host, port = given_args.host, given_args.port
    local_server = ServerThread((host, port))
    local_server.start()

    # l.stop() will stop the looping calls
    #print("trala1")
    #reactor.run()
    #print("trala2")

    while True:
        if not connected:
            print("Trying connection ... ")
            try:
                server.register_dispenser('')
                connected = True
                print("Connected to server.")
            except:
                connected = False
                print("No connection to server.")
        time.sleep(5)


if __name__ == "__main__":
    main()