import unittest
import json
from app import app
from app.rule_engine import RuleEngine

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.rule_engine = RuleEngine()

    def test_handle_event_valid(self):
        # Test handling a valid event
        event_data = {'timestamp': '2023-05-24T05:55:00+00:00', 'is_driving_safe': False, 'location_type': 'highway'}
        response = self.app.post('/event', json=event_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {'message': 'Event received successfully'})
        self.assertIn(event_data, self.rule_engine.database['events'])

    def test_handle_event_invalid_format(self):
        # Test handling an event with invalid format
        invalid_event_data = {'invalid_key': 'invalid_value'}
        response = self.app.post('/event', json=invalid_event_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data), {'error': 'Invalid event format'})

    def test_get_alert_valid(self):
        # Test getting a valid alert
        alert_data = {'id': 1, 'location_type': 'highway', 'timestamp': '2023-05-24T06:00:00+00:00'}
        self.rule_engine.database['alerts'].append(alert_data)
        response = self.app.get('/alert/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), alert_data)

    def test_get_alert_invalid_id(self):
        # Test getting an alert with an invalid ID
        response = self.app.get('/alert/999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data), {'error': 'Alert not found'})

if __name__ == '__main__':
    unittest.main()
