import random

class Incident:
    def __init__(self, incident_id, timestamp, priority):
        self.id = incident_id
        self.timestamp = timestamp
        self.priority = priority  # e.g., "low", "medium", "high"
        self.assigned = False
        self.assigned_level = None
        self.response_time = None
        self.met_sla = None

class IncidentGenerator:
    def __init__(self, env, incident_queue, max_queue_size=100):
        self.env = env
        self.incident_queue = incident_queue
        self.max_queue_size = max_queue_size
        self.incident_count = 0

    def generate(self, interval):
        while True:
            yield self.env.timeout(interval)
            if len(self.incident_queue.items) < self.max_queue_size:
                incident = self._create_incident()
                self.incident_queue.put(incident)
            else:
                print(f"[{self.env.now}] Incident dropped: queue full")

    def _create_incident(self):
        self.incident_count += 1
        priority = random.choices(['low', 'medium', 'high'], weights=[0.5, 0.3, 0.2])[0]
        return Incident(
            incident_id=self.incident_count,
            timestamp=self.env.now,
            priority=priority
        )
