"""
This module contains the callback for making a graph for the weather data in the selected day.
"""
from dash import Output, Input, callback, State
from utils.data_processing import get_datetime_data
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from dash import callback_context as ctx


#callback for making a graf for the weather data in the selected day
@callback(
    [Output("graph", "figure"),
            Output("date-time", "children")
     ],
    [Input("button-day1", "n_clicks"),
     Input("button-day2", "n_clicks"),
     Input("button-day3", "n_clicks"),
     Input("button-day4", "n_clicks"),
     Input("button-day5", "n_clicks"),
     Input("button-day6", "n_clicks"),
     Input("button-day7", "n_clicks"),
     Input("map", "clickData")
     ],
)
def make_graph(n_clicks1, n_clicks2, n_clicks3, n_clicks4, n_clicks5, n_clicks6, n_clicks7, clickData):
    if ctx.triggered_id == 'map':
        button_id = "button-day1"
    else:
        button_id = ctx.triggered_id or 'button-day1'
    date_list = {
        "button-day1": datetime.now().strftime("%Y-%m-%d"),
        "button-day2": (datetime.now() + pd.DateOffset(days=1)).strftime("%Y-%m-%d"),
        "button-day3": (datetime.now() + pd.DateOffset(days=2)).strftime("%Y-%m-%d"),
        "button-day4": (datetime.now() + pd.DateOffset(days=3)).strftime("%Y-%m-%d"),
        "button-day5": (datetime.now() + pd.DateOffset(days=4)).strftime("%Y-%m-%d"),
        "button-day6": (datetime.now() + pd.DateOffset(days=5)).strftime("%Y-%m-%d"),
        "button-day7": (datetime.now() + pd.DateOffset(days=6)).strftime("%Y-%m-%d")
    }
    if clickData is None:
        lat, lon = 50.0755, 14.4378
    else:
        lat, lon = clickData['latlng'].values()
    date = date_list[button_id]
    data = get_datetime_data(lat, lon, date)
    data["datetime"] = pd.to_datetime(data["datetime"], format="%H:%M:%S")
    if data is None or data.empty:
        # Return an empty figure if no data
        return go.Figure(), ""

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data["datetime"],
        y=data["temp"],
        mode="lines+markers+text",
        line=dict(color='gray', width=4),  # line
        marker=dict(color='darkgray', size=8),  # markers
        text = data["temp"][0:24],
        textposition = "top center"
    ))
    fig.update_layout(
        title={
            'text': f"{date}",
            'font': dict(size=20),
        },
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial", size=12, color='white'),
        margin=dict(l=20, r=50, t=0, b=20),
        height=300,
    )
    fig.update_xaxes(showgrid=True, zeroline=True, tickformat="%H:00", gridcolor='rgba(0, 0, 0, 0.3)')
    fig.update_yaxes(showgrid=True, zeroline=False, showticklabels=False, gridcolor='rgba(0, 0, 0, 0.3)')
    fig.update_yaxes()

    if date == datetime.now().strftime("%Y-%m-%d"):
        date = "Today"
    else:
        date = datetime.strptime(date, "%Y-%m-%d").strftime("%d.%m.%Y")
    return fig, date
