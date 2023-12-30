# Enview Application (Backend)

## Project Structure

This project follows the directory structure outlined above:

- **app:** Contains the main application code.
  - `__init__.py`: Initialization file for the app module.
  - `routes.py`: Defines the web routes for handling driving events and alerts.
  - `rule_engine.py`: Implements the rule engine for generating alerts.
  - `database.py`: Defines the in-memory database structure.

- **tests:** Includes unit tests for the app.
  - `__init__.py`: Initialization file for the tests module.
  - `test_routes.py`: Tests for the web routes.
  - `test_rule_engine.py`: Tests for the rule engine.

- **config.py:** Configuration file for the project. (Can be expanded based on project needs)

- **requirements.txt:** Lists project dependencies.

- **run.py:** Script to run the application.


## Getting Started

1. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. Run the application:

    ```bash
    python3 run.py
    ```
## Note:
- For better visibility of the functioning of these codes, you can use Thunder Client for POST and GET
- Copy below link 
    ```bash
    http://127.0.0.1:5000/event
    ```
- Now provide JSON data for posting like the below example
    ```bash
    {
    "timestamp": "2023-12-30T04:48:43",
    "is_driving_safe": false,
    "vehicle_id": 1238,
    "location_type": "commercial"
    }
    ```
- The above data gets stored in the event of database.json, and then calculating the threshold will generate an alert.
- For GET result, choose the GET option in Thunder Client and then paste the below link
   ```bash
     http://127.0.0.1:5000/alert/alert_id
   ```
## APIs

- **POST /event:** Receive driving events from the IoT device.
- **GET /alert/{alert_id}:** Retrieve a single alert by its ID.

## Running Tests

```bash
python3 -m unittest discover -s tests
