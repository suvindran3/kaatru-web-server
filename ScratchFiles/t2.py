import openrouteservice
from openrouteservice import convert
import folium
import webbrowser
from k_id_functions import k_id_generator
import pandas
import numpy


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

client = openrouteservice.Client(key='5b3ce3597851110001cf6248a43578774b6045098866145a1bb76279')

coords = ((80.2707, 13.0827),(77.5946,12.9716))

res = client.directions(coords)
geometry = client.directions(coords)['routes'][0]['geometry']
decoded = convert.decode_polyline(geometry)
fastest_route = decoded["coordinates"]

aggregate = 0
for coordinates in fastest_route:
    pollutant = get_value(coordinates[0],coordinates[1])
    aggregate += pollutant

distance_txt = "<h4> <b>Distance :&nbsp" + "<strong>"+str(round(res['routes'][0]['summary']['distance']/1000,1))+" Km </strong>" +"</h4></b>"
# duration_txt = "<h4> <b>Duration :&nbsp" + "<strong>"+str(round(res['routes'][0]['summary']['duration']/60,1))+" Mins. </strong>" +"</h4></b>"
polloution_txt = "<h4> <b>Aggregate Pollution :&nbsp" + "<strong>"+str(round(aggregate,1))+" micrograms/cm3. </strong>" +"</h4></b>"

m = folium.Map(location=[13.0827, 80.2707],zoom_start=7, control_scale=True,tiles="cartodbpositron")
folium.GeoJson(decoded).add_child(folium.Popup(distance_txt+polloution_txt,max_width=300)).add_to(m)

folium.Marker(
    location=list(coords[0][::-1]),
    popup="Chennai",
    icon=folium.Icon(color="green"),
).add_to(m)

folium.Marker(
    location=list(coords[-1][::-1]),
    popup="Bengaluru",
    icon=folium.Icon(color="red"),
).add_to(m)


#coords= ((80.2707, 13.0827),(78.7314574024606, 12.796248841235979), (77.5946,12.9716))

coords= ((80.2707, 13.0827),(78.93265, 13.02715), (77.5946,12.9716))
res = client.directions(coords)
geometry = client.directions(coords)['routes'][0]['geometry']
decoded = convert.decode_polyline(geometry)
fastest_route = decoded["coordinates"]

aggregate = 0
for coordinates in fastest_route:
    pollutant = get_value(coordinates[0],coordinates[1])
    aggregate += pollutant

distance_txt = "<h4> <b>Distance :&nbsp" + "<strong>"+str(round(res['routes'][0]['summary']['distance']/1000,1))+" Km </strong>" +"</h4></b>"
# duration_txt = "<h4> <b>Duration :&nbsp" + "<strong>"+str(round(res['routes'][0]['summary']['duration']/60,1))+" Mins. </strong>" +"</h4></b>"
polloution_txt = "<h4> <b>Aggregate Pollution :&nbsp" + "<strong>"+str(round(aggregate,1))+" micrograms/cm3. </strong>" +"</h4></b>"

folium.GeoJson(decoded).add_child(folium.Popup(distance_txt+polloution_txt,max_width=300)).add_to(m)

m.add_child(folium.LatLngPopup())

m.save('map.html')
webbrowser.open('map.html')

x = openrouteservice.geocode.pelias_reverse(client, point=(80.2707, 13.0827), circle_radius=None, sources=None, layers=None, country=None, size=None, validate=True, dry_run=None)

x["features"][0]["properties"]["locality"]

text = "Chennai"
w = openrouteservice.geocode.pelias_search(client, text, focus_point=None, rect_min_x=None, rect_min_y=None, rect_max_x=None, rect_max_y=None, circle_point=None, circle_radius=None, sources=None, layers=None, country=None, size=None, validate=True, dry_run=None)
w['bbox']

longitude =(w['bbox'][0] + w['bbox'][2])/2
latitude =  (w['bbox'][1] + w['bbox'][3])/2

origin = (longitude, latitude)
