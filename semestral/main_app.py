# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import requests
import plotly.graph_objects as go
import dash_leaflet as dl


def get_data(lat, lon):
    # Actual weather
    weather_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{lat},{lon}?key=SEUTDBMZLD5MPNAAU6PJJQA2E&unitGroup=metric"
    response = requests.get(weather_url)
    data = response.json()
    return data


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
        autosize=True
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
        dbc.Col(dl.Map(id='map',
            children=[
            dl.TileLayer()
        ], center=[50.0755, 14.4378], zoom=10, style={'height': '50vh'}),
            width=6),
        dbc.Col([
            dbc.Input(id="search-bar", type="text", placeholder="Hledat místo", className="mb-2"),
            dbc.Card([
                dbc.CardBody([
                    dbc.Col(html.H5(children="Current Weather:", className="card-title", style={"font-size": "30px"} ), width=6),
                    dbc.Row([
                        dbc.Col(html.Img(src="", id="forecast-icon", style={"width": "30px", "height": "30px"}), style={"max-width": "32px"}),
                        dbc.Col(html.P(children="", id="current-weather",
                                        className="card-text", style={"font-size": "24px"}), width=11),
                    ]),
                    html.P(children="", id="weather-details", className="card-text"),
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


@callback(
    [Output("current-weather", "children"),
     Output("weather-details", "children"),
     Output("forecast-icon", "src"),
     ],
    [Input("map", "clickData")],
    prevent_initial_call=True
)
def update_weather(clickData):
    if clickData is not None:
        lat, lon = clickData['latlng'].values()

        # Get current weather
        weather_data = get_data(lat, lon)
        if weather_data is None:
            return "Failed to get weather data", ""

        temp = weather_data["currentConditions"]["temp"]
        icon = weather_data["currentConditions"]["icon"]
        feels_like = weather_data["currentConditions"]["feelslike"]
        humidity = weather_data["currentConditions"]["humidity"]
        conditions = weather_data["currentConditions"]["conditions"]

        icon_url = f"assets/icons/1st Set - Color/{icon}.png"
        current_weather = f"{temp}°C, Feels like: {feels_like}°C"
        weather_details = f"Conditions: {conditions.capitalize()}, Humidity: {humidity}%"

        return current_weather, weather_details, icon_url

    return "Click on the map to see weather details", ""


if __name__ == '__main__':
    app.run(debug=True)
