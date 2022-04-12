#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 12:50:57 2022

@author: abhijeet
"""
import folium
import webbrowser
import pandas

from folium.plugins import HeatMap


class Map:
    def __init__(self, center, zoom_start):
        self.center = center
        self.zoom_start = zoom_start

    def showMap(self):
        #Create the map
        my_map = folium.Map(location = self.center, zoom_start = self.zoom_start)

        #Display the map
        my_map.save("map.html")
        webbrowser.open("map.html")


#Define coordinates of where we want to center our map
coords = [20.5, 78.5]
map = Map(center = coords, zoom_start = 10)
map.showMap()


class Map(folium.Map):

    def __init__(self, map_center, zoom_start):
        self._map_center = map_center
        self._zoom_start = zoom_start

    def get_map_center(self):
        return self._map_center

    def get_zoom_start(self):
        return self._zoom_start

    def createMap(self):
        map = folium.Map(location=self.get_map_center(), zoom_start=self.get_zoom_start())
        return map

    def get_htmlMap(self):
        return self.createMap()._repr_html_()

    # def add_child(self, map_object):
    #     return self.createMap.add_child(map_object)

# html_map = map_object._repr_html_()
coords = (22.21, 75.321)
zoom_start = 5

data_load_path = "/home/abhijeet/Ranjan/Data/CSV-MAIAC-18-Dec-India/consolidated_data.csv"
aod_data = pandas.read_csv(data_load_path)

india_map = Map(map_center=coords, zoom_start=zoom_start)
heatmap = HeatMap(list(zip(
                        aod_data["latitude"],
                        aod_data["longitude"],
                        aod_data["aod"])),
                        min_opacity=0.2,
                        max_val=max(aod_data["aod"]),
                        radius=20,
                        blur=20)

india_map.add_child(heatmap)

import pandas
path = "/home/abhijeet/Ranjan/Data/CSV-MAIAC-18-Dec-India/pan_india_map_v1_data.csv"
data = pandas.read_csv(path)
