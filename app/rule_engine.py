from datetime import datetime, timedelta
from .database import in_memory_database

class RuleEngine:
    def __init__(self):
        self.database = in_memory_database

    def store_event(self, event):
        self.database['events'].append(event)

    def get_alert(self, alert_id):
        return next((alert for alert in self.database['alerts'] if alert['id'] == alert_id), None)

    def run_rule(self):
        current_time = datetime.utcnow()

        # Evaluate events in the past 5 minutes
        relevant_events = [event for event in self.database['events'] if
                           current_time - timedelta(minutes=5) <= datetime.fromisoformat(event['timestamp']) <= current_time]

        # Check if an alert was generated in the past 5 minutes
        if 'last_alert_time' in self.database and current_time - self.database['last_alert_time'] <= timedelta(minutes=5):
            return

        # Iterate through location types and check the conditions
        for location_type, threshold in self.database['location_thresholds'].items():
            violation_count = sum(1 for event in relevant_events if
                                  event['is_driving_safe'] is False and event['location_type'] == location_type)

            if violation_count >= threshold:
                # Generate and store alert
                alert = {'id': len(self.database['alerts']) + 1, 'location_type': location_type, 'timestamp': str(current_time)}
                self.database['alerts'].append(alert)

                # Update last alert time
                self.database['last_alert_time'] = current_time
                break
