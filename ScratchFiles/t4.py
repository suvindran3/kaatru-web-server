#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 11:12:55 2022

@author: abhijeet

This code can be used to find route.
"""

import openrouteservice
from openrouteservice import convert
import pandas
import numpy
from k_id_functions import k_id_generator
from folium.plugins import MousePosition
import folium
import webbrowser

data_load_path = "/home/abhijeet/Ranjan/Data/CSV-MAIAC-18-Dec-India/interpolated_aod.csv"
aod_data = pandas.read_csv(data_load_path)

aod_data.drop(['Unnamed: 0'], axis=1, inplace=True)
data = aod_data.set_index(["k_id"])

@numpy.vectorize
def get_value(longitude, latitude, data=data):
    k_id = k_id_generator(longitude, latitude)
    try:
        extracted_data = data.loc[k_id]
        return extracted_data[2]
    except KeyError:
        return 0.0

# coords = ((80.2707, 13.0827),(77.5946,12.9716))

client = openrouteservice.Client(key='5b3ce3597851110001cf6248a43578774b6045098866145a1bb76279') # Specify your personal API key

# decode_polyline needs the geometry only
# geometry = client.directions(coords)['routes'][0]['geometry']

# fastest = convert.decode_polyline(geometry)["coordinates"]


origin = input("Enter origin coordinate: ")
origin = tuple(map(float, origin.split(",")))

destination = input("Enter destination coordinate: ")
origin = tuple(map(float, origin.split(",")))

coords = ((80.2707, 13.0827),(77.5946,12.9716))

geometry = client.directions(coords)['routes'][0]['geometry']

fastest_route = convert.decode_polyline(geometry)["coordinates"]

aggregate = 0
for coordinates in fastest_route:
    pollutant = get_value(coordinates[0],coordinates[1])
    aggregate += pollutant

print(aggregate)


coords = ((80.2707, 13.0827),(77.1025, 28.7041))
res = client.directions(coords)
geometry = client.directions(coords)['routes'][0]['geometry']
decoded = convert.decode_polyline(geometry)

distance_txt = "<h4> <b>Distance :&nbsp" + "<strong>"+str(round(res['routes'][0]['summary']['distance']/1000,1))+" Km </strong>" +"</h4></b>"
duration_txt = "<h4> <b>Duration :&nbsp" + "<strong>"+str(round(res['routes'][0]['summary']['duration']/60,1))+" Mins. </strong>" +"</h4></b>"

fastest_route = decoded["coordinates"]

aggregate = 0
for coordinates in fastest_route:
    pollutant = get_value(coordinates[0],coordinates[1])
    aggregate += pollutant

print(aggregate)

distance_txt = "<h4> <b>Distance :&nbsp" + "<strong>"+str(round(res['routes'][0]['summary']['distance']/1000,1))+" Km </strong>" +"</h4></b>"
duration_txt = "<h4> <b>Duration :&nbsp" + "<strong>"+str(round(res['routes'][0]['summary']['duration']/60,1))+" Mins. </strong>" +"</h4></b>"
polloution_txt = "<h4> <b>Aggregate Pollution :&nbsp" + "<strong>"+str(round(aggregate,1))+" micrograms/cm3. </strong>" +"</h4></b>"

map_center = (77.5946,12.9716)

route_map = folium.Map(location=map_center,zoom_start=8, control_scale=True,tiles="cartodbpositron")
folium.GeoJson(decoded).add_child(folium.Popup(distance_txt+duration_txt+polloution_txt,max_width=300)).add_to(route_map)

formatter = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"

MousePosition(
    position='topright',
    separator=' | ',
    empty_string='NaN',
    lng_first=True,
    num_digits=20,
    prefix='Coordinates:',
    lat_formatter=formatter,
    lng_formatter=formatter,
).add_to(route_map)

route_map.save('map.html')
webbrowser.open('map.html')