import requests
from random import sample as sampler
from openrouteservice import convert
import numpy
import pandas
from k_id_functions import k_id_generator

# path of the .csv file
data_load_path = "consolidated_data.csv"
pm_data = pandas.read_csv(data_load_path)

# set index to k_id
data = pm_data.set_index(["k_id"])


@numpy.vectorize
def get_value(longitude, latitude):
    k_id = k_id_generator(longitude, latitude)
    try:
        extracted_data = data.loc[k_id]
        return extracted_data[2]
    except KeyError:
        return 0.0


def alternate_routes(source: list, destination: list) -> dict:
    """
    source = [latitude, longitude]
    destination = [latitude, longitude]

    returns a dictionary with alternate routes
    """

    result = {
        'routes': []
    }
    response = requests.get(
        f'https://routing.openstreetmap.de/routed-car/route/v1/driving/{source[1]},{source[0]};{destination[1]},'
        f'{destination[0]}?alternatives=true&steps=true')

    try:
        for route in response.json()['routes']:
            coordinates = []
            for points in route['legs'][0]['steps']:
                decoded = convert.decode_polyline(points['geometry'])
                for latlng in decoded['coordinates']:
                    coordinates.append(
                        {
                            'lat': latlng[1],
                            'lng': latlng[0],

                        }
                    )
            result['routes'].append(coordinates)

    except KeyError:
        print('key error')
    return result


def get(origin: list, destination: list) -> dict:

    """
        source = [latitude, longitude]
        destination = [latitude, longitude]

        returns a json with routes and the respective pm2.5 data

        """

    res = {
      'data': []
    }
    routes = alternate_routes(origin, destination)['routes']
    aggregate = 0
    sampling_ratio = 0
    for route in routes:
        if len(route) <= 6500:
            sampling_ratio = len(route) // 15
        elif 6500 < len(route) <= 10000:
            sampling_ratio = len(route) // 30
        sample = sampler(route, sampling_ratio)
        for coordinates in sample:
            aggregate += get_value(coordinates['lng'], coordinates['lat'])
        aggregate *= sampling_ratio
        res['data'].append(
            {
                'aggregate': aggregate,
                'coordinates': route
            }
        )
    return res


# Test
# source = [13.0836939, 80.270186]  # latitude, longitude
# destination = [19.0759899, 72.8773928]  # latitude, longitude
# a = routing(origin=source, destination=destination)
