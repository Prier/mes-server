#!/usr/bin/env python
__author__ = 'armienn'


class MesResource():
    def __init__(self):
        self.taken = False
        self.boundToOrder = 0


class Order():
    def __init__(self, order, robot):
        self.order = order
        self.allocatedArea = []
        self.allocatedRobot = robot
        self.status = 'unstarted'


class ResourceHandler():
    def __init__(self):
        self.active_orders = []
        self.resources = {
            'Dispenser': MesResource(),
            'Ramp': MesResource(),
            'Line': MesResource(),
            'Floor': MesResource(),
            'Station1': MesResource(),
            'Station2': MesResource(),
            'Station3': MesResource(),
            'LoadOff1': MesResource(),
            'LoadOff2': MesResource(),
            'LoadOff3': MesResource(),
            'Mobile1': MesResource(),
            'Mobile2': MesResource(),
            'Mobile3': MesResource(),
            'Cell1': MesResource(),
            'Cell2': MesResource(),
            'Cell3': MesResource()
        }
        print 'Initialised resources'

    def get_mobile_robot(self, number):
        return self.resources['Mobile'+str(number)]

    @staticmethod
    def get_mobile_robot_name(number):
        return 'Mobile'+str(number)

    @staticmethod
    def get_command(next_order, robot_name, m_status):
        new_order = Order(next_order, robot_name)
        print 'what ??!'