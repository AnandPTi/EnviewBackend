import unittest
from app.rule_engine import RuleEngine
from datetime import datetime, timedelta

class TestRuleEngine(unittest.TestCase):
    def setUp(self):
        self.rule_engine = RuleEngine()

    def test_store_event(self):
        # Test storing an event
        event = {'timestamp': '2023-05-24T05:55:00+00:00', 'is_driving_safe': False, 'location_type': 'highway', 'vehicle_id': 'ABC123'}
        self.rule_engine.store_event(event)
        # Check if the event is stored in the database
        self.assertIn(event, self.rule_engine.database['events'])

    def test_get_alert(self):
        # Test getting an alert
        alert = {'id': 1, 'location_type': 'highway', 'timestamp': '2023-05-24T06:00:00+00:00'}
        self.rule_engine.database['alerts'].append(alert)
        retrieved_alert = self.rule_engine.get_alert(1)
        self.assertEqual(alert, retrieved_alert)

    def test_run_rule_no_events(self):
        # Test running the rule engine with no events
        self.rule_engine.run_rule()
        self.assertEqual(len(self.rule_engine.database['alerts']), 0)

    def test_run_rule_single_event(self):
        # Test running the rule engine with a single event
        event = {'timestamp': '2023-05-24T05:55:00+00:00', 'is_driving_safe': False, 'location_type': 'highway', 'vehicle_id': 'ABC123'}
        self.rule_engine.store_event(event)
        self.rule_engine.run_rule()
        self.assertEqual(len(self.rule_engine.database['alerts']), 0)

    def test_run_rule_multiple_events_no_alert(self):
        # Test running the rule engine with multiple events but no alert should be generated
        events = [
            {'timestamp': '2023-05-24T05:55:00+00:00', 'is_driving_safe': False, 'location_type': 'highway', 'vehicle_id': 'ABC123'},
            {'timestamp': '2023-05-24T05:56:00+00:00', 'is_driving_safe': False, 'location_type': 'highway', 'vehicle_id': 'ABC123'},
            {'timestamp': '2023-05-24T05:57:00+00:00', 'is_driving_safe': False, 'location_type': 'highway', 'vehicle_id': 'ABC123'},
        ]
        for event in events:
            self.rule_engine.store_event(event)
        self.rule_engine.run_rule()
        self.assertEqual(len(self.rule_engine.database['alerts']), 0)

    def test_run_rule_generate_alert(self):
        # Test running the rule engine where an alert should be generated
        events = [
            {'timestamp': '2023-05-24T05:55:00+00:00', 'is_driving_safe': False, 'location_type': 'residential', 'vehicle_id': 'ABC123'},
            {'timestamp': '2023-05-24T05:56:00+00:00', 'is_driving_safe': False, 'location_type': 'residential', 'vehicle_id': 'ABC123'},
            {'timestamp': '2023-05-24T05:57:00+00:00', 'is_driving_safe': False, 'location_type': 'residential', 'vehicle_id': 'ABC123'},
            {'timestamp': '2023-05-24T05:58:00+00:00', 'is_driving_safe': False, 'location_type': 'residential', 'vehicle_id': 'ABC123'},
        ]
        for event in events:
            self.rule_engine.store_event(event)
        self.rule_engine.run_rule()
        self.assertEqual(len(self.rule_engine.database['alerts']), 1)

    def test_run_rule_multiple_location_types(self):
        # Test running the rule engine with events from different location types
        events = [
            {'timestamp': '2023-05-24T05:55:00+00:00', 'is_driving_safe': False, 'location_type': 'highway', 'vehicle_id': 'ABC123'},
            {'timestamp': '2023-05-24T05:56:00+00:00', 'is_driving_safe': False, 'location_type': 'city_center', 'vehicle_id': 'ABC123'},
            {'timestamp': '2023-05-24T05:57:00+00:00', 'is_driving_safe': False, 'location_type': 'commercial', 'vehicle_id': 'ABC123'},
            {'timestamp': '2023-05-24T05:58:00+00:00', 'is_driving_safe': False, 'location_type': 'residential', 'vehicle_id': 'ABC123'},
        ]
        for event in events:
            self.rule_engine.store_event(event)
        self.rule_engine.run_rule()
        self.assertEqual(len(self.rule_engine.database['alerts']), 4)

    def test_run_rule_multiple_runs_within_5_minutes(self):
        # Test running the rule engine multiple times within 5 minutes and ensure no additional alerts are generated
        event = {'timestamp': '2023-05-24T05:55:00+00:00', 'is_driving_safe': False, 'location_type': 'highway', 'vehicle_id': 'ABC123'}
        self.rule_engine.store_event(event)
        self.rule_engine.run_rule()
        self.rule_engine.run_rule()
        self.assertEqual(len(self.rule_engine.database['alerts']), 1)

    def test_run_rule_alert_generated_after_5_minutes(self):
        # Test running the rule engine where an alert is generated after the 5-minute window
        past_time = datetime.utcnow() - timedelta(minutes=6)
        event = {'timestamp': past_time.isoformat(), 'is_driving_safe': False, 'location_type': 'highway', 'vehicle_id': 'ABC123'}
        self.rule_engine.store_event(event)
        self.rule_engine.run_rule()
        self.assertEqual(len(self.rule_engine.database['alerts']), 1)

if __name__ == '__main__':
    unittest.main()
