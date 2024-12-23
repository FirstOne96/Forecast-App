"""
This module initializes the Dash app and imports all callbacks.
"""
from dash import Dash
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "Weather App"

from app.callbacks import *  # Import all callbacks
