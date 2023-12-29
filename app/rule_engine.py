from datetime import datetime, timedelta
import json
import pytz

class RuleEngine:
    def __init__(self, database_file='app/database.json'):
        self.database_file = database_file
        self.load_data()

    def load_data(self):
        try:
            with open(self.database_file, 'r') as file:
                self.database = json.load(file)
        except FileNotFoundError:
            self.database = {
                'events': [],
                'alerts': [],
                'location_thresholds': {
                    'highway': 4,
                    'city_center': 3,
                    'commercial': 2,
                    'residential': 1,
                },
            }

    def save_data(self):
        with open(self.database_file, 'w') as file:
            json.dump(self.database, file, indent=2)

    def store_event(self, event):
        self.load_data()
        self.database['events'].append(event)
        self.save_data()

    def get_alert(self, alert_id):
        return next((alert for alert in self.database['alerts'] if alert['id'] == alert_id), None)

    def run_rule(self):
        #current_time = datetime.utcnow()
        current_time = datetime.utcnow().replace(microsecond=0, tzinfo=pytz.utc)
        print(current_time)
        print(datetime.fromisoformat('2023-12-28T08:52:21').replace(microsecond=0, tzinfo=pytz.utc))
        print(timedelta(minutes=5))
        # Evaluate events in the past 5 minutes
        relevant_events = [event for event in self.database['events'] if
                           current_time - timedelta(minutes=5) <= datetime.fromisoformat(event['timestamp']).replace(microsecond=0, tzinfo=pytz.utc) <= current_time]
        #comments
        print("Relevant Events:")
        for event in relevant_events:
            print(event)

        # Check if an alert was generated in the past 5 minutes
        if 'last_alert_time' in self.database and current_time - datetime.fromisoformat(self.database['last_alert_time']) <= timedelta(minutes=5):
            return

        # Iterate through location types and check the conditions
        for location_type, threshold in self.database['location_thresholds'].items():
            violation_count = sum(1 for event in relevant_events if
                                  event.get('is_driving_safe', False) is False and event.get('location_type') == location_type)

            #comments
            print(f"Violation Count for {location_type}: {violation_count}")

            if violation_count >= threshold:
                # Generate and store alert
                alert = {'id': len(self.database['alerts']) + 1, 'location_type': location_type, 'timestamp': str(current_time)}
                self.database['alerts'].append(alert)

                # Update last alert time
                self.database['last_alert_time'] = str(current_time)
                self.save_data()
                break





# from datetime import datetime, timedelta
# from .database import in_memory_database

# class RuleEngine:
#     def __init__(self):
#         self.database = in_memory_database

#     def store_event(self, event):
#         self.database['events'].append(event)

#     def get_alert(self, alert_id):
#         return next((alert for alert in self.database['alerts'] if alert['id'] == alert_id), None)

#     def run_rule(self):
#         current_time = datetime.utcnow()

#         # Evaluate events in the past 5 minutes
#         relevant_events = [event for event in self.database['events'] if
#                            current_time - timedelta(minutes=5) <= datetime.fromisoformat(event['timestamp']) <= current_time]

#         # Check if an alert was generated in the past 5 minutes
#         if 'last_alert_time' in self.database and current_time - self.database['last_alert_time'] <= timedelta(minutes=5):
#             return

#         # Iterate through location types and check the conditions
#         for location_type, threshold in self.database['location_thresholds'].items():
#             violation_count = sum(1 for event in relevant_events if
#                                   event['is_driving_safe'] is False and event['location_type'] == location_type)

#             if violation_count >= threshold:
#                 # Generate and store alert
#                 alert = {'id': len(self.database['alerts']) + 1, 'location_type': location_type, 'timestamp': str(current_time)}
#                 self.database['alerts'].append(alert)

#                 # Update last alert time
#                 self.database['last_alert_time'] = current_time
#                 break
