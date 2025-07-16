import simpy
from .incident import IncidentGenerator
from .staff import StaffPool

class DataCenterSimulator:
    def __init__(self, config):
        self.env = simpy.Environment()
        self.config = config
        self.incident_queue = simpy.Store(self.env)
        self.staff_pool = StaffPool(self.env, config["staffing"])
        self.incident_gen = IncidentGenerator(
            self.env,
            self.incident_queue,
            max_queue_size=config.get("max_queue_size", 100)
        )
        self.results = []

    def run(self, until=480):
        self.env.process(self.incident_gen.generate(interval=self.config["incident_interval"]))
        self.env.process(self.incident_dispatch_loop())
        self.env.run(until=until)

    def incident_dispatch_loop(self):
        while True:
            incident = yield self.incident_queue.get()
            self.env.process(self.handle_incident(incident))

    def handle_incident(self, incident):
        level = self.determine_required_level(incident)
        staff = yield self.staff_pool.request_staff(level)
        response_time = self.env.now - incident.timestamp
        yield self.env.timeout(self.config["handling_time"][level])
        self.release_staff(level, staff)

        self.record_result(incident, response_time, level)

    def determine_required_level(self, incident):
        if incident.priority == "high":
            return "L3"
        elif incident.priority == "medium":
            return "L2"
        else:
            return "L1"

    def release_staff(self, level, staff):
        self.staff_pool.release_staff(level, staff)

    def record_result(self, incident, response_time, level):
        self.results.append({
            "incident_id": incident.id,
            "timestamp": incident.timestamp,
            "priority": incident.priority,
            "response_time": response_time,
            "handled_by": level,
        })
