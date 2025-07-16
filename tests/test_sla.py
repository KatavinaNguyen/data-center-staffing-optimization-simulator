import unittest
from datetime import datetime, timedelta
from src import analytics

class TestSLACalculations(unittest.TestCase):

    def setUp(self):
        # Reset logs before each test
        analytics.sla_log.clear()
        analytics.incident_log.clear()

    def test_sla_met(self):
        start = datetime(2023, 1, 1, 9, 0, 0)
        end = start + timedelta(minutes=4)
        analytics.log_incident(start, end, role_assigned='L1', sla_threshold=timedelta(minutes=5))

        self.assertEqual(len(analytics.sla_log), 1)
        self.assertEqual(analytics.sla_log[0], ('L1', True))
        self.assertTrue(analytics.incident_log[0]['sla_met'])

    def test_sla_not_met(self):
        start = datetime(2023, 1, 1, 10, 0, 0)
        end = start + timedelta(minutes=8)
        analytics.log_incident(start, end, role_assigned='L2', sla_threshold=timedelta(minutes=5))

        self.assertEqual(len(analytics.sla_log), 1)
        self.assertEqual(analytics.sla_log[0], ('L2', False))
        self.assertFalse(analytics.incident_log[0]['sla_met'])

    def test_multiple_roles_sla(self):
        base_time = datetime(2023, 1, 1, 12, 0, 0)
        analytics.log_incident(base_time, base_time + timedelta(minutes=3), 'L1', timedelta(minutes=5))
        analytics.log_incident(base_time, base_time + timedelta(minutes=6), 'L2', timedelta(minutes=5))
        analytics.log_incident(base_time, base_time + timedelta(minutes=4), 'L3', timedelta(minutes=6))
        analytics.log_incident(base_time, base_time + timedelta(minutes=7), 'L3', timedelta(minutes=6))

        met_counts = {
            'L1': True,
            'L2': False,
            'L3': [True, False]
        }

        self.assertEqual(len(analytics.sla_log), 4)
        self.assertEqual(analytics.sla_log[0], ('L1', True))
        self.assertEqual(analytics.sla_log[1], ('L2', False))
        self.assertEqual(analytics.sla_log[2], ('L3', True))
        self.assertEqual(analytics.sla_log[3], ('L3', False))

if __name__ == '__main__':
    unittest.main()
