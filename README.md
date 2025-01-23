## Weather Forecast Application

### Description

The Weather Forecast Application is an interactive web-based tool that provides:

Real-time weather updates for a selected location.

A 7-day weather forecast.

Interactive map features for location-based weather information.

Additional details such as humidity, wind speed, and cloudiness.

The application also includes future potential features like clothing advice based on weather conditions.

### Features

Real-time weather updates: Displays the current temperature, weather conditions, and other metrics for a selected location.

7-day weather forecast: Shows the maximum and minimum temperatures, along with weather icons, for the upcoming week.

Interactive map: Allows users to click on locations to retrieve weather data.

Search bar: Search for weather information by entering city names.

### Dependencies

The application requires the following dependencies, which are listed in the requirements.txt file:

- dash

- dash-bootstrap-components

- dash-leaflet

- geopy

- pandas

- plotly

- requests

- pytest (for running tests)

#### To install all required dependencies, use:

pip install -r requirements.txt

### How to Start the Application

Clone the repository:

git clone <repository-url>
cd <repository-directory>

### Set up your environment:

python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

### Run the application:

python main_app.py

Open a web browser and navigate to http://127.0.0.1:8050.

### How to Run Tests

Tests are located in the tests/ directory and written using pytest.

Activate your virtual environment (if not already activated).

### Run the tests:

pytest

This will execute all test cases and provide a summary of the results.

### Known Issues

Multilingual support is not yet implemented.

Advanced forecasting features like precipitation graphs are pending development.

Clothing advice is currently disabled due to unresolved API issues.
