# -*- coding: utf-8 -*-
import simpy
import pandas as pd

#|Production line object
class Line(object):

    #|Set line name and unit per second rate
    def __init__(self, env, name, rate):
        self.env = env
        self.name = name
        self.rate = rate
        self.log = pd.DataFrame()

    #|Set store object as either input or output
    def set_store(self, store, mode):
        if mode == 'in':
            self.ins = store
        if mode =='out':
            self.out = store

    #|Run simpy simulation process
    def run(self, amount, start):
        yield self.env.timeout(int(start-self.env.now))
        in_req = self.ins.r.request()
        out_req = self.out.r.request()
        yield in_req
        yield out_req
        astart = self.env.now
        yield self.ins.c.get(amount)
        yield self.env.timeout(amount/self.rate)
        yield self.out.c.put(amount)
        self.ins.r.release(in_req)
        self.out.r.release(out_req)
        end = self.env.now
        log = {'line':self.name, 'amount':amount, 'input':self.ins.name,'output':self.out.name,
                'plan_start':start, 'actu_start':astart, 'end':end}
        self.log = self.log.append(log, ignore_index=True)

#|Storage object
class Store(object):

    def __init__(self, env, name, cap, lvl, limit):
        self.env = env
        self.name = name
        self.c = simpy.Container(env, cap, lvl)
        self.r = simpy.Resource(env, limit)


