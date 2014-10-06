__author__ = 'prier'

import xmlrpclib
import datetime

server = xmlrpclib.ServerProxy('http://localhost:8000', use_datetime=True)
today = datetime.datetime.today()

cell_status = {
    'cell_id': 2,
    'event': 'Free',
    'time': str(today),
}

mobile_status = {
    'robot_id': 3,
    'event': 'Free',
    'time': str(today),
    'batt_level': 80,
}

print (server.cell_status(cell_status))
print (server.mobile_status(mobile_status))

