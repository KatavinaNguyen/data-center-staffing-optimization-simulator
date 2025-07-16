class StaffMember:
    def __init__(self, env, role):
        self.role = role
        self.resource = simpy.Resource(env, capacity=1)

def create_staff_pool(env, config):
    pool = []
    for role in ['L1', 'L2', 'L3']:
        for _ in range(config['staffing'][role]):
            pool.append(StaffMember(env, role))
    return pool
