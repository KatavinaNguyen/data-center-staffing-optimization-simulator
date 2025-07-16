import random

def generate_incidents(env, staff_pool, config):
    def incident_process():
        while True:
            yield env.timeout(random.expovariate(config['incident_rate']))
            # logic for staff assignment
    env.process(incident_process())
