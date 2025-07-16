import unittest
import simpy
from datetime import datetime, timedelta
from src.simulator import Incident, handle_incident
from src.analytics import sla_log, incident_log

class MockEnv:
    def __init__(self):
        self.now = 0  # time in minutes
        self.events = []

    def timeout(self, duration):
        self.now += duration
        return duration

class TestSimulator(unittest.TestCase):

    def setUp(self):
        self.env = MockEnv()
        sla_log.clear()
        incident_log.clear()

    def test_incident_creation(self):
        incident = Incident(id=1, arrival_time=10, duration=5, role_required='L1')
        self.assertEqual(incident.id, 1)
        self.assertEqual(incident.arrival_time, 10)
        self.assertEqual(incident.duration, 5)
        self.assertEqual(incident.role_required, 'L1')

    def test_handle_incident_meets_sla(self):
        incident = Incident(id=1, arrival_time=0, duration=3, role_required='L1')
        handle_incident(self.env, incident, sla_threshold=timedelta(minutes=5))
        self.assertEqual(len(sla_log), 1)
        self.assertTrue(sla_log[0][1])  # SLA met

    def test_handle_incident_violates_sla(self):
        incident = Incident(id=2, arrival_time=0, duration=7, role_required='L2')
        handle_incident(self.env, incident, sla_threshold=timedelta(minutes=5))
        self.assertEqual(len(sla_log), 1)
        self.assertFalse(sla_log[0][1])  # SLA violated

    def test_multiple_incidents(self):
        inc1 = Incident(id=1, arrival_time=0, duration=4, role_required='L1')
        inc2 = Incident(id=2, arrival_time=5, duration=6, role_required='L2')
        handle_incident(self.env, inc1, sla_threshold=timedelta(minutes=5))
        handle_incident(self.env, inc2, sla_threshold=timedelta(minutes=5))

        self.assertEqual(len(sla_log), 2)
        self.assertTrue(sla_log[0][1])  # SLA met
        self.assertFalse(sla_log[1][1])  # SLA violated

if __name__ == '__main__':
    unittest.main()
