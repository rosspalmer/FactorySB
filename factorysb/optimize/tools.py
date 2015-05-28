import random

def random_job_list(factory, mode='all'):
    job_sum = {}
    for product_name in factory.ord['product_name'].unique():
        job_sum[product_name] = 0
    for line_name in factory.lines:
        if line_name not in factory.job_list:
            factory.job_list[line_name] = []
    if mode == 'all':
        while len(job_sum) > 0:
            for line in factory.lines:
                if len(job_sum) > 0:
                    rand = random.choice(job_sum.keys())
                    factory.job_list[line].append(rand)
                    job_sum[rand] += factory.prod[rand]['job_amount']
                    if job_sum[rand] >= \
                    factory.ord[factory.ord['product_name'] == rand]['amount'].sum():
                        del job_sum[rand]
    elif mode == 'switch':
        l_line = random.choice(factory.lines.keys())
        l_loc = random.randint(0, len(factory.job_list[l_line])-1)
        l_job = factory.job_list[l_line][l_loc]
        r_line = random.choice(factory.lines.keys())
        r_loc = random.randint(0, len(factory.job_list[r_line])-1)
        r_job = factory.job_list[r_line][r_loc]

        factory.job_list[l_line][l_loc] = r_job
        factory.job_list[r_line][r_loc] = l_job

    return factory


def costs(factory):
    idle = factory.log['idle'].sum()
    fine = factory.ord['total_fee'].sum()
    total = idle + fine
    cost_dic = {'idle':idle, 'fine':fine, 'total':total}
    return cost_dic
