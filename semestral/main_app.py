# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import requests
import plotly.graph_objects as go


def get_data():
    api_key = "0dec1cf6b8743419a0936245d1db9dea"
    city = "Praha"
    # Actual weather
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"


def get_historical_data(lat, lon, start_date, end_date):
    timemachine_url = f"https://archive-api.open-meteo.com/v1/era5?latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}&hourly=temperature_2m"
    timemachine_response = requests.get(timemachine_url)
    timemachine_data = timemachine_response.json()
    return timemachine_data


# Geocoding ( get latitude and longitude of the city )
def geocoding(city, api_key):
    geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={api_key}"
    geocoding_response = requests.get(geocoding_url)
    geocoding_data = geocoding_response.json()
    lat = geocoding_data[0]["lat"]
    lon = geocoding_data[0]["lon"]


def world_map():
    fig = go.Figure(go.Scattergeo())
    fig.update_geos(
        showland=True,
        landcolor="rgb(212, 212, 212)",
        showocean=True, oceancolor="LightBlue",
        showcountries=True,
        showcoastlines=True,
        coastlinecolor="Gray",
    )
    fig.update_layout(
        height=300,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        autosize = True
    )
    return fig


def forecast_graph():
    pass


app = Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY])
app.title = "Weather App"

app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col(html.H2("Temperature by coordinates", className="text-info mt-2    ", style={"textAlign": "left", }),
                width=10, ),
    ]),
    # Map and search bar
    dbc.Row([
        dbc.Col(dcc.Graph(id="world-map",
                          style={"padding": "0px", "margin": "0px", "height": "100%", "width": "100%"},
                          figure=world_map()),
                width=6),
        dbc.Col([
            dbc.Input(id="search-bar", type="text", placeholder="Hledat místo", className="mb-2"),
            dbc.Card([
                dbc.CardBody([
                    html.H5("Aktuální počasí", className="card-title"),
                    html.P("🌞 TODO", id="current-weather", className="card-text"),
                    html.P("TODO", id="weather-details", className="card-text"),
                ])
            ])
        ], width=6)
    ], className="mt-2", style={"padding": "0px", "margin": "0px", "height": "100%", "width": "100%"}),
    # Middle section
    dbc.Row([
        dbc.Col(html.Div(id='forecast-title', className="text-info mt-2", children="7-days forecast"), width=12),
        dbc.Col(dcc.Graph(id='forecast-graph'), width=12),
    ], className="mt-2"),
    dbc.Row([
        dbc.Col([
            html.H5("Podrobnosti o počasí", className="text-warning"),
            dbc.Card([
                dbc.CardBody([
                    html.P("Pocitová teplota: ...", id="feels-like"),
                    html.P("Vlhkost: ...", id="humidity"),
                    html.P("Oblačnost: ...", id="cloudiness"),
                ])
            ])
        ], width=6),
        dbc.Col([
            html.H5("Chat GPT (Telling what to wear)", className="text-warning"),
            dbc.Card([
                dbc.CardBody([
                    dcc.Textarea(id="wear-suggestion", style={"width": "100%", "height": "200px"}),
                ])
            ])
        ], width=6)
    ], className="mt-4")
], fluid=True)

if __name__ == '__main__':
    app.run(debug=True)
