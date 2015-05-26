import factorysb as fsb

fac = fsb.Factory()

#|Create products and define job amount, job time, and transport time
fac.create_product('A', 100, 200, 50)
fac.create_product('B', 50, 250, 30)
fac.create_product('C', 200, 300, 100)

#|Create input and output inventories
i_inv = [{'name':'A', 'amount':10000}]
i_inv.append({'name':'B', 'amount':10000})
i_inv.append({'name':'C', 'amount':10000})
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

#|Create random job list for Lines
fac.job_list = fsb.random_job_list(fac, 20)

for i in fac.prod.values():
    print i

for i in fac.job_list:
    print i
    print fac.job_list[i]

fac.run('out')
print fac.log

for c in fac.stores['in'].c:
    print 'Input - %s: %s' % (c, fac.stores['in'].c[c].level)

for c in fac.stores['out'].c:
    print 'Output - %s: %s' % (c, fac.stores['out'].c[c].level)

print 'Total Idle: %s' % str(fac.log['idle'].sum())

