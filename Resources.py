#!/usr/bin/env python
__author__ = 'armienn & reaver'

OS_NOT_STARTED = 0
OS_TO_DISP = 1
OS_WAIT_FOR_DISP = 2
OS_TO_CELL = 3
OS_WAIT_FOR_CELL = 4
OS_READY_TO_SORT = 5
OS_TIP = 6
OS_SORTING = 7
OS_WAIT_FOR_MOBILE = 8
OS_LOAD = 9
OS_LOADING_NAUW = 10
OS_RETURN = 11

class MesResource():
    def __init__(self, to_dispenser, to_cell):
        self.taken = False
        self.bound_to_order = 0
        self.to_dispenser = to_dispenser
        self.to_cell = to_cell


class Order():
    def __init__(self, resources, starting_area, order, robot, cell):
        self.order = order
        self.allocated_cell = cell
        self.allocated_robot = robot
        self.allocated_areas = []
        self.allocated_areas.append(starting_area)
        resources[starting_area].taken = True
        resources[starting_area].bound_to_order = self
        resources[robot].bound_to_order = self
        resources[robot].taken = True
        resources[cell].bound_to_order = self
        resources[cell].taken = True
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
            resources[area].bound_to_order = 0
        self.allocated_areas = []
        resources[self.allocated_robot].bound_to_order = 0
        resources[self.allocated_robot].taken = False
        self.allocated_robot = 0

    def deallocate_cell(self, resources):
        resources[self.allocated_cell].taken = False
        resources[self.allocated_cell].bound_to_order = 0
        self.allocated_cell = 0

    def end(self, resources):
        self.order = 0
        self.status = 0
        for area in self.allocated_areas:
            resources[area].taken = False
            resources[area].bound_to_order = 0
        self.allocated_areas = []
        resources[self.allocated_robot].bound_to_order = 0
        resources[self.allocated_robot].taken = False
        self.allocated_robot = 0
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

    def get_order(self, robot_name, m_status, order_queue):
        current_pos = m_status['position']
        order = self.resources['Cell1'].bound_to_order
        if order == 0:
            order = self.resources['Cell2'].bound_to_order
        if order == 0:
            order = self.resources['Cell3'].bound_to_order

        if order != 0:
            if order.status == OS_WAIT_FOR_MOBILE:
                order.allocate(self.resources, current_pos, robot_name)
            elif order.status == OS_TO_DISP and order.allocated_robot == 0:
                order.allocate(self.resources, current_pos, robot_name)
        else:
            free_cell = 0
            if self.resources['Cell1'].bound_to_order == 0:
                free_cell = 'Cell1'
            if free_cell == 0:
                if self.resources['Cell2'].bound_to_order == 0:
                    free_cell = 'Cell2'
            if free_cell == 0:
                if self.resources['Cell3'].bound_to_order == 0:
                    free_cell = 'Cell3'
            if free_cell != 0:
                if not order_queue.empty():
                    order = order_queue.get()
                    order = Order(self.resources, current_pos, order, robot_name, free_cell)

        return order

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
            print 'processed mobile command for order status OS_NOT_STARTED'

        elif current_order.status == OS_TO_DISP:
            current_order.allocate(self.resources, current_pos, robot_name)
            next_pos = self.resources[current_pos].to_dispenser
            if next_pos == 1:  # at the dispenser
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
            print 'processed mobile command for order status OS_TO_DISP'

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
            print 'processed mobile command for order status OS_WAIT_FOR_DISP'

        elif current_order.status == OS_TO_CELL:
            current_order.allocate(self.resources, current_pos, robot_name)
            next_pos = self.resources[current_pos].to_cell
            if next_pos == 1:  # at a cell
                current_order.status = OS_WAIT_FOR_CELL
                command = {
                    'command': 'COMMAND_WAIT'
                }

            elif next_pos == 2:  # next to the three cells
                next_pos = 0
                if current_order.allocated_cell == 'Cell1':
                    next_pos = 'LoadOff1'
                elif current_order.allocated_cell == 'Cell2':
                    next_pos = 'LoadOff2'
                elif current_order.allocated_cell == 'Cell3':
                    next_pos = 'LoadOff3'

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
                    #this really shouldn't happen!
                    next_pos = next_pos
            else:
                if not self.resources[next_pos].taken:
                    current_order.allocate(self.resources, next_pos, robot_name)
                    command = {
                        'command': 'COMMAND_NAVIGATE',
                        'path': next_pos
                    }
            print 'processed mobile command for order status OS_TO_CELL'

        elif current_order.status == OS_WAIT_FOR_CELL:
            current_order.allocate(self.resources, current_pos, robot_name)
            command = {
                'command': 'COMMAND_WAIT'
            }
            print 'processed mobile command for order status OS_WAIT_FOR_CELL'

        elif current_order.status == OS_READY_TO_SORT:
            current_order.allocate(self.resources, current_pos, robot_name)
            current_order.status = OS_TIP
            command = {
                'command': 'COMMAND_TIP'
            }
            print 'processed mobile command for order status OS_WAIT_FOR_CELL'

        elif current_order.status == OS_TIP:
            current_order.status = OS_SORTING
            print 'processed mobile command for order status OS_TIP'

        elif current_order.status == OS_SORTING:
            #  we shouldn't get here from the mobile platform
            print 'I AM ERROR: Mobile platform bound to order that is sorting'

        elif current_order.status == OS_WAIT_FOR_MOBILE:
            current_order.allocate(self.resources, current_pos, robot_name)
            next_pos = self.resources[current_pos].to_cell
            if next_pos == 1:  # at a cell
                current_order.status = OS_LOAD
                command = {
                    'command': 'COMMAND_WAIT'
                }

            elif next_pos == 2:  # next to the three cells
                next_pos = 0
                if current_order.allocated_cell == 'Cell1':
                    next_pos = 'LoadOff1'
                elif current_order.allocated_cell == 'Cell2':
                    next_pos = 'LoadOff2'
                elif current_order.allocated_cell == 'Cell3':
                    next_pos = 'LoadOff3'

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
                    #this really shouldn't happen!
                    next_pos = next_pos
            else:
                if not self.resources[next_pos].taken:
                    current_order.allocate(self.resources, next_pos, robot_name)
                    command = {
                        'command': 'COMMAND_NAVIGATE',
                        'path': next_pos
                    }
            print 'processed mobile command for order status OS_WAIT_FOR_MOBILE'

        elif current_order.status == OS_LOAD:
            command = {
                'command': 'COMMAND_WAIT'
            }
            print 'processed mobile command for order status OS_LOAD'

        elif current_order.status == OS_RETURN:
            #TODO: Find out what the mobile robot is actually supposed to do with the bricks
            current_order.end(self.resources)

            #current_order.allocate(self.resources, current_pos, robot_name)
            #next_pos = self.resources[current_pos].to_dispenser
            #if next_pos == 1:  # at the dispenser
            #    print 'At dispenser for drop-off'
            #
            #    command = {
            #        'command': 'COMMAND_WAIT'
            #    }
            #else:
            #    if not self.resources[next_pos].taken:
            #        current_order.allocate(self.resources, next_pos, robot_name)
            #        command = {
            #            'command': 'COMMAND_NAVIGATE',
            #            'path': next_pos
            #        }
            print 'processed mobile command for order status OS_RETURN'

        else:
            print 'I AM ERROR: Failed to process mobile command: unknown order status'
        
        if command == 0:
            command = {
                'command': 'COMMAND_WAIT'
            }
        print 'Finished finding command'
        return command

    def get_command_c_free(self, robot_name, c_status):
        current_order = self.resources[robot_name].bound_to_order
        command = 0

        if current_order.status == OS_WAIT_FOR_CELL:
            command = {
                'command': 'COMMAND_SORTBRICKS',
                'order': current_order.order
            }
            print 'Processed command for OS_SORT'
        elif current_order.status == OS_LOAD:
            command = dict(command='COMMAND_LOADBRICKS')
            print 'Processed command for OS_LOAD'
        elif current_order.status == OS_WAIT_FOR_MOBILE:
            command = dict(command='COMMAND_WAIT')
            print 'processed command for OS_WAIT_FOR_MOBILE'
        elif current_order.status == OS_LOADING_NAUW:
            current_order.status = OS_RETURN
            command = dict(command='COMMAND_WAIT')
            print 'processed command for OS_LOADING_NAUW'
        else:
            print 'No commands processed'

        return command

    def get_command_c_sorting(self, robot_name):
        current_order = self.resources[robot_name].bound_to_order
        command = 0

        if current_order.status == OS_READY_TO_SORT:
            current_order.status = OS_SORTING
            command = dict(command='COMMAND_SORTBRICKS')
            print 'Updated state from OS_READY_TO_SORT to OS_SORTING'
        elif current_order.status == OS_SORTING:
            command = dict(command='COMMAND_SORTBRICKS')
            print 'Still sorting'
        else:
            print 'I AM ERROR.'

        return command

    def get_command_c_done_sorting(self, robot_name):
        current_order = self.resources[robot_name].bound_to_order
        command = 0

        if current_order.status == OS_SORTING:
            current_order.status = OS_WAIT_FOR_MOBILE
            command = dict(command='COMMAND_WAIT')
            print 'Updated state from OS_SORT to OS_WAIT_FOR_MOBILE'
        elif current_order.status == OS_WAIT_FOR_MOBILE:
            command = dict(command='COMMAND_WAIT')
            print 'Still waiting for mobile'
        elif current_order.status == OS_LOAD:
            command = dict(command='COMMAND_LOADBRICKS')
            print 'Start loading bricks'
        else:
            print 'I AM ERROR.'

        return command

    def get_command_c_out_of_bricks(self, robot_name):
        current_order = self.resources[robot_name].bound_to_order
        command = 0

        if current_order.status == OS_SORTING:
            current_order.status = OS_TO_DISP
            print 'Updated state from OS_SORT to OS_TO_DISP'
        elif current_order.status == OS_WAIT_FOR_CELL:
            command = {
                'command': 'COMMAND_SORTBRICKS',
                'order': current_order.order
            }
            print 'Processed command for OS_WAIT_FOR_CELL'
        else:
            print 'No commands processed'

        return command

    def get_command_c_loading_bricks(self, robot_name):
        current_order = self.resources[robot_name].bound_to_order

        if current_order.status == OS_LOAD:
            current_order.status = OS_LOADING_NAUW
            print 'Updated state from OS_LOAD to OS_LOADING_NAUW'
        else:
            print 'I AM ERROR.'


def get_mobile_robot_name(number):
    return 'Mobile'+str(number)


def get_cell_robot_name(number):
    return 'Cell'+str(number)