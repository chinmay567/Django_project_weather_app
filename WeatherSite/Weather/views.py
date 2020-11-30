from django.shortcuts import render
import pandas as pd
import requests
import json

# Create your views here.


def index(request):
    df = pd.read_csv('worldcities.csv')
    if 'city' in request.GET:
        city = request.GET['city']
        if df[df['city_ascii'] == city]['city_ascii'].any():
            lat = df[df['city_ascii'] == city]['lat']
            lon = df[df['city_ascii'] == city]['lng']

            url = "https://climacell-microweather-v1.p.rapidapi.com/weather/realtime"

            querystring = {"lat": lat,
                           "lon": lon,
                           "unit_system": "si",
                           "fields": ["precipitation", "precipitation_type", "temp", "cloud_cover", "wind_speed", "weather_code"]}

            headers = {
                'x-rapidapi-key': "352be8204cmsh420bf815735b8e4p1bc629jsn808401126bbd",
                'x-rapidapi-host': "climacell-microweather-v1.p.rapidapi.com"
            }

            response = requests.request(
                "GET", url, headers=headers, params=querystring).json()

            context = {
                'city_name': city,
                'temp': response['temp']['value'],
                'weather_code': response['weather_code']['value'],
                'wind_speed': response['wind_speed']['value'],
                'precipitation_type': response['precipitation_type']['value']
            }
        else:
            context = None
    else:
        context = None
    return render(request, 'Weather/index.html', context)
