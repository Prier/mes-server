__author__ = 'prier'

import xmlrpclib
import datetime

server = xmlrpclib.ServerProxy('http://localhost:8000', use_datetime=True)
today = datetime.datetime.today()
print (server.status('2', 'Free', str(today)))
