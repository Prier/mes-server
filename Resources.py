#!/usr/bin/env python
__author__ = 'armienn'

OS_NOT_STARTED = 0
OS_TO_DISP = 1
OS_WAIT_FOR_DISP = 2
OS_TO_CELL = 3
OS_WAIT_FOR_CELL = 4
OS_TIP = 5
OS_SORT = 6
OS_WAIT_FOR_MOBILE = 7
OS_LOAD = 8


class MesResource():
    def __init__(self, to_dispenser, to_cell):
        self.taken = False
        self.bound_to_order = 0
        self.to_dispenser = to_dispenser
        self.to_cell = to_cell


class Order():
    def __init__(self, resources, starting_area, order, robot):
        self.order = order
        self.allocated_robot = robot
        self.allocated_areas = [starting_area]
        resources[starting_area].taken = True
        resources[starting_area].bound_to_order = self
        resources[robot].bound_to_order = self
        self.status = OS_NOT_STARTED

    def allocate(self, resources, area, robot):
        self.allocated_areas.append(area)
        self.allocated_robot = robot
        resources[area].taken = True
        resources[area].bound_to_order = self
        resources[robot].bound_to_order = self

    def deallocate(self, resources):
        for area in self.allocated_areas:
            resources[area].taken = False
        self.allocated_areas = []
        resources[self.allocated_robot].bound_to_order = 0


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

    def get_new_command_m(self, next_order, robot_name, m_status):
        new_order = Order(next_order, robot_name)
        current_pos = m_status['position']
        next_pos = self.resources[current_pos].to_dispenser
        command = 0
        if not self.resources[next_pos].taken:
            new_order.allocate(self.resources, next_pos, robot_name)
            command = {
                'command': 'COMMAND_NAVIGATE',
                'path': next_pos
            }
        return command

    def get_command_m(self, robot_name, m_status):
        current_order = self.resources[robot_name].bound_to_order
        current_pos = m_status['position']
        current_order.deallocate(self.resources)
        if current_order.status == OS_NOT_STARTED:
            print 'what ??!'
        elif current_order.status == OS_TO_DISP:
            print 'what ??!'
        elif current_order.status == OS_WAIT_FOR_DISP:
            print 'what ??!'
        elif current_order.status == OS_TO_CELL:
            print 'what ??!'
        elif current_order.status == OS_WAIT_FOR_CELL:
            print 'what ??!'
        elif current_order.status == OS_TIP:
            print 'what ??!'
        elif current_order.status == OS_SORT:
            print 'what ??!'
        else:
            print 'what ??!'
        print 'what ??!'

    def get_new_command_c(self, next_order, robot_name, c_status):
        new_order = Order(next_order, robot_name)

    def get_command_c(self, robot_name, c_status):
        current_order = self.resources[robot_name].bound_to_order
        print 'what ??!'


def get_mobile_robot_name(number):
    return 'Mobile'+str(number)


def get_cell_robot_name(number):
    return 'Cell'+str(number)