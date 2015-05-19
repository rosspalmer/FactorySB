# -*- coding: utf-8 -*-
import comp

import simpy

#|Factory object used to combine lines and stores,
#|create job orders, and run simulation
class Factory(object):

    def __init__(self):
        self.env = simpy.Environment()
        self.line = {}
        self.store = {}
        self.order = []

    def add_line(self, name, rate):
        self.line[name] = comp.Line(self.env, name, rate)

    def add_store(self, name, cap, lvl=0, limit=1):
        self.store[name] = comp.Store(self.env, name, cap, lvl, limit)

    def add_order(self, line, instore, outstore, amount, start):
        self.order.append({'line':line, 'instore':instore,
            'outstore':outstore, 'amount':amount,'start':start})

    def run(self, until):
        for odr in self.order:
            self.line[odr['line']].set_store(self.store[odr['instore']], 'in')
            self.line[odr['line']].set_store(self.store[odr['outstore']], 'out')
            self.env.process(self.line[odr['line']].run(odr['amount'], odr['start']))
        self.env.run(until=until)
