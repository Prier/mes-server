__author__ = 'prier'

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import cgi
import random
import threading
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, XML
from xml.etree import ElementTree
from xml.dom import minidom
import sys
import datetime
import re
lastNum = re.compile(r'(?:[^\d]*(\d+)[^\d]*)+')

ord_num = "00001"
last_ord_num = "00001"

HOST = 'localhost'
PORT = 21212

def increment(s):
    """ look for the last sequence of number(s) in a string and increment """
    m = lastNum.search(s)
    if m:
        next = str(int(m.group(1))+1)
        start, end = m.span(1)
        s = s[:max(end-len(next), start)] + next + s[end:]
    return s

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def gen_new_order():
    global ord_num, last_ord_num
    ord_num = last_ord_num
    last_ord_num = increment(ord_num)
    ord_xxxxx = SubElement(orders, 'ord_'+ord_num)

    order = SubElement(ord_xxxxx, 'order')

    time = SubElement(order, 'time')
    time.text = str(datetime.datetime.now())

    bricks = SubElement(order, 'bricks')
    red = SubElement(bricks, 'red')
    red.text = str(random.randint(1, 5))
    yellow = SubElement(bricks, 'yellow')
    yellow.text = str(random.randint(1, 5))
    green = SubElement(bricks, 'green')
    green.text = str(random.randint(1, 5))

    status = SubElement(order, 'status')
    status.text = "ready"

    #print prettify(orders)
    return


############################################################################
'''  One instance per connection.
     Override handle(self) to customize action. '''

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/xml; charset="utf-8"')
        self.end_headers()
        message = threading.currentThread().getName()

        if self.path == '/orders':
            self.wfile.write(prettify(orders))
            self.wfile.write('\n')
        elif self.path == '/':
            self.wfile.write(message)
            self.wfile.write('\n')

        return

    def do_POST(self):
        # Parse the form data posted
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })

        # Begin the response
        self.send_response(301)
        self.end_headers()
        self.wfile.write('Client: %s\n' % str(self.client_address))
        self.wfile.write('User-agent: %s\n' % str(self.headers['user-agent']))
        self.wfile.write('Path: %s\n' % self.path)
        self.wfile.write('Form data:\n')
        return

############################################################################

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
# Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True

############################################################################

if __name__ == "__main__":

    orders = Element('orders')

    gen_new_order()
    gen_new_order()
    gen_new_order()

    print 'Printing generated orders: \n'
    print prettify(orders)

    server = ThreadedHTTPServer((HOST, PORT), Handler)
    # terminate with Ctrl-C
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)

############################################################################
