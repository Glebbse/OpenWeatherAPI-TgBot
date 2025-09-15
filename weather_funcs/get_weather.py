import os

import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
api = os.getenv("API_KEY")

def get_geo(*, city:str):
    url_geo = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api}"
    try:
        response_geo = requests.get(url=url_geo, timeout=10)
        response_geo.raise_for_status()
    except requests.exceptions.RequestException as err:
        print(f"Coordinates request error {err}")
    geo_data = response_geo.json()
    if not geo_data:
        print(f"City {city} hasn't been found.")
    return geo_data[0]["lat"], geo_data[0]["lon"]

def get_weather(*, lat:float, lon: float):
    url_weather =f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=daily,hourly,minutely&appid={api}"
    try:
        response_weather = requests.get(url=url_weather, params={"units": "metric", "lang": "ru"}, timeout=10)
        response_weather.raise_for_status()
    except requests.exceptions.RequestException as err:
        print(f"Weather request error {err}")
    return response_weather.json()

def format_weather(*, city: str, data: dict):
    result = [f"City/Город: {city}", f"GMT/Часовой пояс: {data['timezone']}"]
    current = data["current"]
    for i, key in enumerate(current):
        if key == "dt":
            result.append(f"date time: {datetime.fromtimestamp(current.get(key))}")
            continue
        if key in ("sunrise", "sunset"):
            result.append(f"{key}: {datetime.fromtimestamp(current.get(key))}")
            continue
        if key == "weather":
            result.append(f"Описание: {current['weather'][0]['description']}")
            continue
        result.append(f"{key}: {current.get(key)}")
    return "\n".join(result)