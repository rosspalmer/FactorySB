import factorysb as fsb
import random as rn

fac = fsb.Factory()

#|Create products and define job amount, job time, and transport time
fac.create_product('A', 100, 200, 50)
fac.create_product('B', 50, 400, 30)
fac.create_product('C', 80, 300, 100)

#|Create input and output inventories
i_inv = [{'name':'A', 'amount':50000}]
i_inv.append({'name':'B', 'amount':50000})
i_inv.append({'name':'C', 'amount':50000})
o_inv = [{'name':'A', 'amount':0}]
o_inv.append({'name':'B', 'amount':0})
o_inv.append({'name':'C', 'amount':0})

#|Create input and output Stores
fac.create_store('in', i_inv)
fac.create_store('out', o_inv)

#|Create Lines
fac.create_line('line1', 'in', 'out')
fac.create_line('line2', 'in', 'out')
fac.create_line('line3', 'in', 'out')

for i in range(10):
    fac.create_order(rn.choice(fac.prod.keys()), rn.randint(200,400),
            rn.randint(1000,10000), rn.randint(4000,6000))

fsb.brute_random(fac, 100)

#for c in fac.stores['in'].c:
    #print 'Input - %s: %s' % (c, fac.stores['in'].c[c].level)

#for c in fac.stores['out'].c:
    #print 'Output - %s: %s' % (c, fac.stores['out'].c[c].level)

#print 'Total Idle: %s' % str(fac.log['idle'].sum())

#