"""
This module contains functions for fetching weather data from the Visual Crossing Weather API.
"""
import requests

API_KEY = "SLU3NEK44RZHES6CQK7U7H7QS"

def fetch_current_weather_data(lat, lon):
    weather_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{lat},{lon}?key={API_KEY}&unitGroup=metric"
    response = requests.get(weather_url)
    return response.json() if response.status_code == 200 else None

def fetch_forecast_data(lat, lon):
    forecast_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{lat},{lon}/next7days?unitGroup=metric&key={API_KEY}&unitGroup=metric"
    response = requests.get(forecast_url)
    return response.json() if response.status_code == 200 else None

def fetch_datetime_data(lat, lon, date):
    datetime_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{lat},{lon}/{date}?key={API_KEY}&unitGroup=metric"
    response = requests.get(datetime_url)
    return response.json() if response.status_code == 200 else None
