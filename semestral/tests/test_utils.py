"""
This module contains tests for the utility functions in the app.
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.data_processing import get_current_weather_data, get_forecast_data, get_datetime_data
from utils.geolocation import geolocator


# Test get_current_weather_data
def test_get_current_weather_data():
    # Mock API response
    lat, lon = 50.0755, 14.4378
    result = get_current_weather_data(lat, lon)
    assert result["temp"] is not None
    assert result["feelslike"] is not None
    assert result["icon"] is not None


# Test get_7day_forecast
def test_get_forecast_data():
    lat, lon = 50.0755, 14.4378
    result = get_forecast_data(lat, lon)
    assert len(result) != 0
    assert result["tempmax"][0] != 0
    assert result["icon"][1] is not None

def test_get_datetime_data():
    lat, lon = 50.0755, 14.4378
    date = "2022-05-01"
    result = get_datetime_data(lat, lon, date)
    assert len(result) != 0
    assert result["temp"][0] is not None
    assert result["icon"][1] is not None


# Test geolocator
def test_geolocator():
    lat, lon = 50.0755, 14.4378
    result = geolocator(lat, lon)
    assert result == "Capital City of Prague, Czechia"
