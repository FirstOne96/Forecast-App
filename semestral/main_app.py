# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import requests
import plotly.graph_objects as go


api_key = "0dec1cf6b8743419a0936245d1db9dea"
city = "Praha"
# Actual weather
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

# Geocoding ( get latitude and longitude of the city )
geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={api_key}"
geocoding_response = requests.get(geocoding_url)
geocoding_data = geocoding_response.json()
lat = geocoding_data[0]["lat"]
lon = geocoding_data[0]["lon"]


start_date = "2021-01-01"
end_date = "2021-12-31"

# Historical weather
timemachine_url = f"https://archive-api.open-meteo.com/v1/era5?latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}&hourly=temperature_2m"
timemachine_response = requests.get(timemachine_url)
timemachine_data = timemachine_response.json()

response = requests.get(url)
data = response.json()
print(f"Weather in {city}: {data['main']['temp']}°C")

current_temp = data["main"]["temp"]

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

fig = go.Figure(go.Scattergeo())
fig.add_trace(go.Scattergeo())

fig.update_geos(
    projection_type="orthographic",
    showland=True,
    showcoastlines=True,
    showcountries=True, countrycolor="black",
    showocean=True, oceancolor="LightBlue",
    landcolor="rgb(230, 230, 230)",
    coastlinecolor="grey")


fig.update_layout(
    autosize=True,
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    height=500
)



app.layout = dbc.Container(
    [
    html.H1(f"Weather in {city}: {current_temp}°C"),
    html.Hr(),
    dbc.Row(
        dbc.Col(dcc.Graph(id="world-map", figure=fig), md = 6)
        )
    ],
    fluid=True,
)

if __name__ == '__main__':
    app.run(debug=True)