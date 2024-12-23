"""
This module contains tests for the callback functions in the app.
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.callbacks import update_weather, update_forecast, update_weather_from_search

def test_update_weather():
    # Test if the function returns a dictionary
    clickData = {'containerPoint': {'x': 380, 'y': 200},
                 'latlng': {'lat': 50.10296448723355, 'lng': 14.345397949218752}, 'layerPoint': {'x': 380, 'y': 200}}
    result = update_weather(clickData, False)
    assert result is not None

def test_update_forecast():
    # Test if the function returns a dictionary
    clickData = {'containerPoint': {'x': 380, 'y': 200},
                 'latlng': {'lat': 50.10296448723355, 'lng': 14.345397949218752}, 'layerPoint': {'x': 380, 'y': 200}}
    result = update_forecast(clickData)
    assert result is not None
