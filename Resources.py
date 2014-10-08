#!/usr/bin/env python
__author__ = 'armienn'

class MesResource():
    def __init__(self):
        self.taken = False
        self.boundToOrder = 0
        troloro = 0

resources = { 
    'Dispenser' : MesResource(),
    'Ramp' : MesResource(),
    'Line' : MesResource(),
    'Floor' : MesResource(),
    'Station1' : MesResource(),
    'Station2' : MesResource(),
    'Station3' : MesResource(),
    'LoadOff1' : MesResource(),
    'LoadOff2' : MesResource(),
    'LoadOff3' : MesResource(),
    'Mobile1' : MesResource(),
    'Mobile2' : MesResource(),
    'Mobile3' : MesResource(),
    'Cell1' : MesResource(),
    'Cell2' : MesResource(),
    'Cell3' : MesResource()
}


