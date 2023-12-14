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
    python run.py
    ```

## APIs

- **POST /event:** Receive driving events from the IoT device.
- **GET /alert/{alert_id}:** Retrieve a single alert by its ID.

## Running Tests

```bash
python -m unittest discover -s tests
