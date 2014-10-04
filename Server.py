__author__ = 'prier'

import argparse
import threading
from SimpleXMLRPCServer import SimpleXMLRPCServer

# MES functions

def get_orders(x,y):
    return x+y

def status(cell_id, event, time):
    stat = " Cell ID: "+cell_id+"\n Event:"+event+"\n Time: "+time
    print stat

class ServerThread(threading.Thread):
    def __init__(self, server_addr):
        threading.Thread.__init__(self)
        self.server = SimpleXMLRPCServer(server_addr, logRequests=True, allow_none=True)
        self.server.register_multicall_functions()
        self.server.register_function(status, 'status')
    def run(self):
        self.server.serve_forever()

def run_server(host, port):
    # server code
    server_addr = (host, port)
    server = ServerThread(server_addr)
    server.start() # The server is now running
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

if __name__ == "__main__":
    main()
