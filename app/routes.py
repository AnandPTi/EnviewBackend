from flask import request, jsonify
from app import app
from .rule_engine import RuleEngine

rule_engine = RuleEngine()

@app.route('/event', methods=['POST'])
def handle_event():
    data = request.get_json()

    if not data or 'timestamp' not in data or 'is_driving_safe' not in data or 'location_type' not in data:
        return jsonify({'error': 'Invalid event format'}), 400

    rule_engine.store_event(data)
    rule_engine.run_rule()  # Added to run the rule on each received event
    return jsonify({'message': 'Event received successfully'}), 200

@app.route('/alert/<int:alert_id>', methods=['GET'])
def get_alert(alert_id):
    alert = rule_engine.get_alert(alert_id)

    if not alert:
        return jsonify({'error': 'Alert not found'}), 404

    return jsonify(alert), 200
