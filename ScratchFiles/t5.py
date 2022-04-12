#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 14:28:43 2022

@author: abhijeet
"""

import branca.colormap
from collections import defaultdict
import folium
import webbrowser
from folium.plugins import HeatMap 

map_osm = folium.Map(llocation=[35,110],zoom_start=1)

steps=20
colormap = branca.colormap.linear.YlOrRd_09.scale(0, 1).to_step(steps)
gradient_map=defaultdict(dict)
for i in range(steps):
    gradient_map[1/steps*i] = colormap.rgb_hex_str(1/steps*i)
colormap.add_to(map_osm) #add color bar at the top of the map

HeatMap(data1,gradient = gradient_map).add_to(map_osm) # Add heat map to the previously created map


map_osm.save("map2.html") # Save as html file
webbrowser.open(file_path) # Default browser open