import flask_sock
from flask import Flask, render_template, request, jsonify

import pandas
import numpy
from folium.plugins import HeatMap

import filter_data
import folium
from random import sample as sampler
from static_coordinates import area_coordinates
import openrouteservice
from openrouteservice import convert

from cleanest_route import get as cleanest_route
import weather_data
from k_id_functions import k_id_generator

####################################################################################################################
# data loading and function definition


# aod_data.drop(['Unnamed: 0'], axis=1, inplace=True)

data_load_path = "./consolidated_data.csv"

pm_data = pandas.read_csv(data_load_path)
data = pm_data.set_index(["k_id"])

heat_map_data = pm_data.sample(n=200000)

map_center = (22.8774, 78.1787)
min_zoom = 3
max_zoom = 14
zoom_start = 4

india_map = folium.Map(
    location=map_center,
    min_zoom=min_zoom,
    max_zoom=max_zoom,
    zoom_start=zoom_start,
    width='100%',
    height='100%',
    left='0%',
    top='2%',
    tiles="cartodbpositron")

heatmap = HeatMap(list(zip(
    heat_map_data["latitude"],
    heat_map_data["longitude"],
    heat_map_data["aod"])),
    name="pm2.5",
    min_opacity=0.2,
    radius=20,
    blur=20,
    overlay=False,
    control=False,
    max_zoom=12)

india_heatmap = india_map.add_child(heatmap)
india_html = india_heatmap._repr_html_()

client = openrouteservice.Client(key='5b3ce3597851110001cf6248ece9320a89864c06b250b741b8cb8f11')

app = Flask(__name__)
socket = flask_sock.Sock(app)
web_socket: flask_sock.Server


def down_sampling(fastest_route, aggregate, ratio):
    down_sampling_ratio = len(fastest_route) // ratio
    fastest_route = sampler(fastest_route, down_sampling_ratio)

    for coordinates in fastest_route:
        pollutant = get_value(coordinates[0], coordinates[1])
        aggregate = aggregate + pollutant

    aggregate *= ratio
    print("Aggregate2: ", aggregate)
    return aggregate


def router(origin, destination):
    try:
        # forward path
        origin_coords = area_coordinates(origin)

        print("Origin: ", origin_coords)

        destination_coords = area_coordinates(destination)
        print("Destination: ", destination_coords)

        origin_destination = (origin_coords, destination_coords)

        res = client.directions(origin_destination)
        geometry = client.directions(origin_destination)['routes'][0]['geometry']

        decoded = convert.decode_polyline(geometry)

        fastest_route = decoded["coordinates"]

        print("[+] Route found ...")
        print("[+] Number of coordinates: ", len(fastest_route))

        aggregate = 0
        if len(fastest_route) <= 3000:
            aggregate = down_sampling(fastest_route, aggregate, 10)

        elif 3000 < len(fastest_route) <= 7000:
            aggregate = down_sampling(fastest_route, aggregate, 20)

        elif len(fastest_route) > 7000:
            aggregate = down_sampling(fastest_route, aggregate, 40)

        print("[+] Pollutants aggregated...")
        print("Total: ", aggregate)
        route_map = folium.Map(
            location=map_center,
            min_zoom=min_zoom,
            max_zoom=max_zoom,
            zoom_start=zoom_start,
            width='100%',
            height='100%',
            left='0%',
            top='2%',
            tiles="cartodbpositron")

        distance_km = res['routes'][0]['summary']['distance'] / 1000

        p_per_km = round(aggregate / distance_km, 2)

        total_time = res['routes'][0]['summary']['duration'] / (60 * 60)
        p_per_hr = round(aggregate / total_time, 2)

        print("[+] Statistics calculated...")

        total_exposure = "<h4> <b>Total exposure :&nbsp" + "<strong>" + str(
            round(aggregate, 2)) + " ug/cm3. </strong>" + "</h4></b>"
        distance_txt = "<h4> <b>Distance :&nbsp" + "<strong>" + str(
            round(distance_km, 2)) + " km </strong>" + "</h4></b>"
        pollution_per_km = "<h4> <b>PM2.5/KM :&nbsp" + "<strong>" + str(
            p_per_km) + " (ug/cm3)/km </strong>" + "</h4></b>"
        pollution_per_hr = "<h4> <b>PM2.5/Hr :&nbsp" + "<strong>" + str(
            p_per_hr) + " (ug/cm3)/hr </strong>" + "</h4></b>"

        print("[+] Pop up ready..")

        folium.GeoJson(decoded).add_child(
            folium.Popup(distance_txt + total_exposure + pollution_per_km + pollution_per_hr, max_width=400)).add_to(
            route_map)
        print("[+] Map created...")

        # Markers
        folium.Marker(
            popup=origin,
            location=list(origin_destination[0][::-1]),
            icon=folium.Icon(color="green"),
        ).add_to(route_map)

        folium.Marker(
            location=list(origin_destination[-1][::-1]),
            popup=destination,
            icon=folium.Icon(color="red"),
        ).add_to(route_map)

        route_map = route_map.add_child(heatmap)

        print("[+] Markers added...")
        route_map.save('./templates/folium.html')
        aggregate = round(aggregate, 2)
        return render_template("route_plot.html",
                               aggregate=aggregate,
                               distance_km=distance_km,
                               p_per_km=p_per_km,
                               p_per_hr=p_per_hr
                               )

    except:
        returnJson = {
            "origin": origin,
            "destination": destination,
            "message": "Origin or destination could not be resolved properly"
        }
        return jsonify(returnJson)


@numpy.vectorize
def get_value(longitude, latitude, _data=data):
    k_id = k_id_generator(longitude, latitude)
    try:
        extracted_data = _data.loc[k_id]
        return extracted_data[2]
    except KeyError:
        return 0.0


####################################################################################################################

@app.route('/airmap')
def pan_india_map():
    return render_template("airmap.html", data=filter_data.heatmap_data())


####################################################################################################################


@app.route('/air_quality', methods=["GET"])
def air_quality():
    longitude = numpy.float64(request.args.to_dict()['lng'])
    latitude = numpy.float64(request.args.to_dict()['lat'])
    value = get_value(longitude, latitude)
    return_json = {
        "Longitude": longitude,
        "Latitude": latitude,
        "PM2.5": numpy.float64(value)
    }
    response = jsonify(return_json)
    response.headers.add('Access-Control-Allow-Origin', '*')
    web_socket.send(data=weather_data.get_data(latitude, longitude))
    return response


@app.route('/routing', methods=["GET"])
def routing():
    origin = request.args.to_dict()['origin'].split(',')
    destination = request.args.to_dict()['destination'].split(',')
    response = jsonify(cleanest_route(origin, destination))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/exposure', methods=['GET', 'POST'])
def exposure():
    if request.method == 'GET':
        origin = request.args.to_dict()['origin']
        destination = request.args.to_dict()['destination']

        return router(origin, destination)

    return render_template("route.html", cmap=india_html)


@socket.route('/test')
def test(ws: flask_sock.Server):
    global web_socket
    web_socket = ws
    while web_socket.connected:
        ws.receive()


if __name__ == "__main__":
    app.run(debug=True)
