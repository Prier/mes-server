#!/usr/bin/env python
__author__ = 'armienn'


class MesResource():
    def __init__(self, to_dispenser, to_cell):
        self.taken = False
        self.bound_to_order = 0
        self.to_dispenser = to_dispenser
        self.to_cell = to_cell


class Order():
    def __init__(self, order, robot):
        self.order = order
        self.allocated_area = []
        self.allocated_robot = robot
        self.status = 'unstarted'


class ResourceHandler():
    def __init__(self):
        self.active_orders = []
        self.resources = {
            'Dispenser': MesResource(1, 'Ramp'),
            'Ramp': MesResource('Dispenser', 'Floor'),
            'Line': MesResource('Floor', 2),
            'Floor': MesResource('Ramp', 'Line'),
            'Station1': MesResource('Dispenser', 'Ramp'),
            'Station2': MesResource('Dispenser', 'Ramp'),
            'Station3': MesResource('Dispenser', 'Ramp'),
            'LoadOff1': MesResource('Line', 1),
            'LoadOff2': MesResource('Line', 1),
            'LoadOff3': MesResource('Line', 1),
            'Mobile1': MesResource(0, 0),
            'Mobile2': MesResource(0, 0),
            'Mobile3': MesResource(0, 0),
            'Cell1': MesResource(0, 0),
            'Cell2': MesResource(0, 0),
            'Cell3': MesResource(0, 0)
        }
        print 'Initialised resources'

    def get_mobile_robot(self, number):
        return self.resources['Mobile'+str(number)]

    def get_command_m(self, next_order, robot_name, m_status):
        new_order = Order(next_order, robot_name)
        current_pos = m_status['position']
        print 'what ??!'

    def get_command_m(self, robot_name, m_status):
        current_order = self.resources[robot_name].bound_to_order
        print 'what ??!'

    def get_command_c(self, next_order, robot_name, c_status):
        new_order = Order(next_order, robot_name)
        print 'what ??!'

    def get_command_c(self, robot_name, c_status):
        current_order = self.resources[robot_name].bound_to_order
        print 'what ??!'


def get_mobile_robot_name(number):
    return 'Mobile'+str(number)


def get_cell_robot_name(number):
    return 'Cell'+str(number)