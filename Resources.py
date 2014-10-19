#!/usr/bin/env python
__author__ = 'armienn & reaver'

OS_NOT_STARTED = 0
OS_TO_DISP = 1
OS_WAIT_FOR_DISP = 2
OS_TO_CELL = 3
OS_WAIT_FOR_CELL = 4
OS_TIP = 5
OS_SORT = 6
OS_WAIT_FOR_MOBILE = 7
OS_LOAD = 8

alloc_areas = []

class MesResource():
    def __init__(self, to_dispenser, to_cell):
        self.taken = False
        self.bound_to_order = 0
        self.to_dispenser = to_dispenser
        self.to_cell = to_cell


class Order():
    def __init__(self, resources, starting_area, order, robot):
        self.order = order
        self.allocated_cell = 0
        self.allocated_robot = robot
        alloc_areas.append(starting_area)
        self.allocated_areas = alloc_areas
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

    def allocate_cell(self, resources, cell):
        self.allocated_cell = cell
        resources[cell].taken = True
        resources[cell].bound_to_order = self

    def deallocate_cell(self, resources):
        resources[self.allocated_cell].taken = False
        resources[self.allocated_cell].bound_to_order = 0
        self.allocated_cell = 0


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

    def get_cell_robot(self, number):
        return self.resources['Cell'+str(number)]

    def get_new_command_m(self, next_order, robot_name, m_status):
        current_pos = m_status['position']
        new_order = Order(self.resources, current_pos, next_order, robot_name)
        next_pos = self.resources[current_pos].to_dispenser
        command = 0
        if not self.resources[next_pos].taken:
            new_order.allocate(self.resources, next_pos, robot_name)
            new_order.status = OS_TO_DISP
            command = {
                'command': 'COMMAND_NAVIGATE',
                'path': next_pos
            }
        return command

    def get_command_m(self, robot_name, m_status):
        current_order = self.resources[robot_name].bound_to_order
        current_pos = m_status['position']
        current_order.deallocate(self.resources)
        command = 0

        if current_order.status == OS_NOT_STARTED:
            next_pos = self.resources[current_pos].to_dispenser
            current_order.allocate(self.resources, current_pos, robot_name)
            if not self.resources[next_pos].taken:
                current_order.allocate(self.resources, next_pos, robot_name)
                current_order.status = OS_TO_DISP
                command = {
                    'command': 'COMMAND_NAVIGATE',
                    'path': next_pos
                }
            print 'processed command for order status OS_NOT_STARTED'

        elif current_order.status == OS_TO_DISP:
            current_order.allocate(self.resources, current_pos, robot_name)
            next_pos = self.resources[current_pos].to_dispenser
            if current_pos == 'Dispenser':  # at the dispenser
                print 'at dispenser'
                current_order.status = OS_WAIT_FOR_DISP
                command = {
                    'command': 'COMMAND_WAIT'
                }
            else:
                if not self.resources[next_pos].taken:
                    current_order.allocate(self.resources, next_pos, robot_name)
                    command = {
                        'command': 'COMMAND_NAVIGATE',
                        'path': next_pos
                    }
            print 'processed command for order status OS_TO_DISP'

        elif current_order.status == OS_WAIT_FOR_DISP:
            current_order.allocate(self.resources, current_pos, robot_name)
            dispenser_has_dispensed = True  # TODO: check if bricks have been dispensed
            if dispenser_has_dispensed:
                current_order.status = OS_TO_CELL
                next_pos = self.resources[current_pos].to_cell
                if not self.resources[next_pos].taken:
                    current_order.allocate(self.resources, next_pos, robot_name)
                    command = {
                        'command': 'COMMAND_NAVIGATE',
                        'path': next_pos
                    }
            print 'processed command for order status OS_WAIT_FOR_DISP'

        elif current_order.status == OS_TO_CELL:
            current_order.allocate(self.resources, current_pos, robot_name)
            next_pos = self.resources[current_pos].to_cell
            if current_pos == "Station1" or current_pos == "Station2" or current_pos == "Station3":  # at a cell
                current_order.status = OS_WAIT_FOR_CELL
                command = {
                    'command': 'COMMAND_WAIT'
                }

            elif current_pos == "Line":  # next to the three cells
                if not self.resources['Station1'].taken:
                    next_pos = 'Station1'
                    current_order.allocate_cell(self.resources, 'Cell1')
                elif not self.resources['Station2'].taken:
                    next_pos = 'Station2'
                    current_order.allocate_cell(self.resources, 'Cell2')
                elif not self.resources['Station3'].taken:
                    next_pos = 'Station3'
                    current_order.allocate_cell(self.resources, 'Cell3')
                else:
                    next_pos = 0
                if next_pos != 0:
                    if not self.resources[next_pos].taken:
                        current_order.allocate(self.resources, next_pos, robot_name)
                        command = {
                            'command': 'COMMAND_NAVIGATE',
                            'path': next_pos
                        }
                    else:
                        current_order.deallocate_cell(self.resources)
            else:
                if not self.resources[next_pos].taken:
                    current_order.allocate(self.resources, next_pos, robot_name)
                    command = {
                        'command': 'COMMAND_NAVIGATE',
                        'path': next_pos
                    }
            print 'processed command for order status OS_TO_CELL'

        elif current_order.status == OS_WAIT_FOR_CELL:
            current_order.allocate(self.resources, current_pos, robot_name)
            cell_has_started = True  # TODO: check cell has started
            if cell_has_started:
                current_order.status = OS_TIP
                command = {
                    'command': 'COMMAND_TIP'
                }
            print 'processed command for order status OS_WAIT_FOR_CELL'

        elif current_order.status == OS_TIP:
            current_order.status = OS_SORT
            print 'processed command for order status OS_TIP'

        elif current_order.status == OS_SORT:
            #  we shouldn't get here from the mobile platform
            print 'Something\'s wrong here'
            print 'processed command for order status OS_SORT'

        else:
            print 'unknown order status'
        
        if command == 0:
            command = {
                'command': 'COMMAND_WAIT'
            }
        print 'finished finding command'
        return command

    def get_command_c(self, robot_name, c_status):
        current_order = self.resources[robot_name].bound_to_order
        current_state = c_status['state']
        current_order.deallocate(self.resources)

        if current_order.status == OS_SORT:
            #TODO
            print 'Processed command for OS_SORT'
        elif current_order.status == OS_LOAD:
            #TODO
            print 'Processed command for OS_LOAD'
        elif current_order.status == OS_WAIT_FOR_MOBILE:
            #TODO
            print 'processed command for OS_WAIT_FOR_MOBILE'
        else:
            #TODO
            print 'No commands processed'

    def update_state(self, state):
        print state


def get_mobile_robot_name(number):
    return 'Mobile'+str(number)


def get_cell_robot_name(number):
    return 'Cell'+str(number)