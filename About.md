**Project Description:**

The SafeDrive Alert Service is a robust backend solution designed to enhance road safety for delivery fleets using a driver monitoring system deployed on IoT devices. This service employs a sophisticated Rule Engine to analyze driving events, focusing on instances of unsafe driving behavior. The primary goal is to generate alerts for repeated speed violations, taking into account the severity based on the location type.

**Key Features:**

1. **Event Processing:**
   - The service exposes a `POST /event` API to receive driving events from IoT devices.
   - Events include crucial information such as timestamp, driving safety status, vehicle ID, and location type.

2. **Rule Engine:**
   - A dynamic rule engine evaluates driving events against predefined criteria, ensuring accuracy and relevance.
   - The rule triggers an alert if, within the past 5 minutes:
      - There are a specified number of unsafe driving events.
      - No alert has been generated during this time period.

3. **Alert Generation:**
   - Alerts are generated in response to rule evaluations, emphasizing repeated speed violations.
   - Severity thresholds vary based on the location type (e.g., highway, city center, residential).

4. **Database Integration:**
   - Event and alert data are stored in a database for historical tracking.
   - The system supports a flexible database structure, allowing easy integration with different databases.

5. **Configuration Management:**
   - Location-specific thresholds for generating alerts are not hardcoded but dynamically stored in a database table.
   - This enables easy adjustment of alert criteria without modifying the core codebase.

6. **GET Endpoint for Alerts:**
   - The service provides a `GET /alert/{alert_id}` API to retrieve details of a specific alert by its unique ID.

7. **Timely Alert Generation:**
   - Alerts are generated within a 5-minute after the rule conditions are met, ensuring prompt notification.

**Implementation Details:**

- The backend is built using a FLASK web framework, providing stability and scalability.
- The rule engine ensures alerts are generated based on event frequency and historical data.
- A mock database stores event and alert data, facilitating easy testing and evaluation.

**Advantages:**

- Enhances road safety for delivery fleets by identifying and addressing unsafe driving behavior.
- Offers flexibility through dynamic configuration, allowing easy adjustments to alert thresholds.
- Promotes timely decision-making by providing a real-time view of driving events and generated alerts.

**Note:** The service can be further extended to include additional functionalities, such as analytics dashboards, real-time monitoring, and integration with third-party systems for a comprehensive driver safety solution.
