import json

import requests

API_KEY = 'b4aabf3b5f3a76ac639ba5ab1c763bab'
pol_endpoint = 'http://api.openweathermap.org/data/2.5/air_pollution?'
weather_endpoint = 'https://api.openweathermap.org/data/2.5/weather?units=metric'


def get_data(lat: float, lng: float) -> str:
    pol_params = {
        'lat': lat,
        'lon': lng,
        'appid': API_KEY,
    }
    weather_params = pol_params
    pol_res = requests.get(f'{pol_endpoint}', params=pol_params).json()
    weather_res = requests.get(f'{weather_endpoint}', params=weather_params).json()
    return_res = json.dumps({
        "aqi": pol_res['list'][0]['main']['aqi'],
        "pm2.5": pol_res['list'][0]['components']['pm2_5'],
        "pm10": pol_res['list'][0]['components']['pm10'],
        "o3": pol_res['list'][0]['components']['o3'],
        "no2": pol_res['list'][0]['components']['no2'],
        "so2": pol_res['list'][0]['components']['so2'],
        "co": pol_res['list'][0]['components']['co'],
        "nh3": pol_res['list'][0]['components']['nh3'],
        "temp": weather_res['main']['temp'],
        "feels_like": weather_res['main']['feels_like'],
        "pressure": weather_res['main']['pressure'],
        "humidity": weather_res['main']['humidity'],
        "wind": weather_res['wind']['speed'],
    })
    return return_res

