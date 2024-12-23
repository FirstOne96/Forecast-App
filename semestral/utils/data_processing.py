"""
This module contains functions for processing data fetched from the API.
"""
import pandas as pd

from .api_requests import fetch_current_weather_data, fetch_forecast_data, fetch_datetime_data

def get_current_weather_data(lat, lon):
    data = fetch_current_weather_data(lat, lon)
    if data is None:
        return None
    description = data["description"]
    try:
        df = pd.DataFrame(data["currentConditions"])
    except ValueError as e:
        print("Error creating DataFrame:", e)
        df = pd.DataFrame()
    df.insert(0, "description", description)
    try:
        df.drop(columns=["dew", "datetimeEpoch", "snow", "snowdepth", "winddir", "pressure", "visibility", "solarradiation",
                     "solarenergy", "uvindex", "stations", "sunriseEpoch", "sunsetEpoch"], inplace=True)
    except KeyError as e:
        print("Error dropping columns:", e)
    return df

def get_forecast_data(lat, lon):
    data = fetch_forecast_data(lat, lon)
    if data is None:
        return None
    forecast = data["days"]
    df = pd.DataFrame(forecast)
    df["datetime"] = pd.to_datetime(df["datetime"])
    try:
        df = df.drop(columns=["datetimeEpoch", "feelslikemax", "feelslike", "feelslikemin", "dew", "precip",
                          "precipcover", "snow", "snowdepth", "windgust", "winddir", "pressure",
                          "cloudcover", "visibility", "solarradiation", "solarenergy", "uvindex", "severerisk",
                          "sunriseEpoch", "sunsetEpoch", "stations", "source", "hours"])
    except KeyError as e:
        print("Error dropping columns:", e)
    return df

def get_datetime_data(lat, lon, date):
    data = fetch_datetime_data(lat, lon, date)
    if data is None:
        return None
    df = pd.DataFrame(data["days"][0]['hours'])
    try:
        df.drop(columns=["dew", "datetimeEpoch", "snow", "snowdepth", "winddir", "pressure", "visibility", "solarradiation",
                     "solarenergy", "uvindex", "stations"], inplace=True)
    except KeyError as e:
        print("Error dropping columns:", e)
    return df
