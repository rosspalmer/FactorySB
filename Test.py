# -*- coding: utf-8 -*-
import factorysb as fsb
import simpy
import random

fac = fsb.Factory()
fac.add_store('in_a', 10000, 10000, 3)
fac.add_store('out_a', 10000, 0, 3)
fac.add_line('line_a', 10)
for i in range(20):
    fac.add_order('line_a', 'in_a', 'out_a', random.randint(500,1000), \
                random.randint(0,300))
fac.run(1000)
for l in fac.line.values():
    print l.log
