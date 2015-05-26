import random

def random_job_list(factory, length):
    job_list = {}
    for line in factory.lines:
        jobs = []
        for i in range(length):
            jobs.append(random.choice(factory.prod.keys()))
        job_list[line] = jobs
    return job_list
