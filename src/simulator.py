import simpy
from incident import generate_incidents
from personnel import create_staff_pool
from analytics import log_results

def run_simulation(config):
    env = simpy.Environment()
    staff = create_staff_pool(env, config)
    generate_incidents(env, staff, config)
    env.run(until=config["simulation_duration"])
    log_results()
