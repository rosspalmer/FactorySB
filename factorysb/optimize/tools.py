import random

def random_job_list(factory, length):
    job_list = {}
    for line in factory.lines:
        jobs = []
        for i in range(length):
            jobs.append(random.choice(factory.prod.keys()))
        job_list[line] = jobs
    return job_list

def cost(factory):
    idle = factory.log['idle'].sum()
    fine = factory.ord['total_fine'].sum()
    total = idle + fine
    cost_dic = {'idle':idle, 'fine':fine, 'total':total}
    return cost_dic
