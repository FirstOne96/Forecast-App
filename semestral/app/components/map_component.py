"""
This module contains a function that creates a map component.
"""
import dash_leaflet as dl
def create_map():
    return dl.Map(id='map',
                  children=[
                      dl.TileLayer()
                  ], center=[50.0755, 14.4378], zoom=10, style={'height': '50vh'})
