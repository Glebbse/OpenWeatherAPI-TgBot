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
    if not geo_data or city.isdigit() or any(c.isdigit() for c in city):
        return f"City {city} hasn't been found. Please, enter your city by letters with full official name 😊"
    return geo_data[0]["lat"], geo_data[0]["lon"]

def get_weather(*, lat:float, lon: float, exclude: str):
    url_weather =f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api}"
    try:
        response_weather = requests.get(url=url_weather, params={"units": "metric", "lang": "ru", "exclude": exclude}, timeout=10)
        response_weather.raise_for_status()
    except requests.exceptions.RequestException as err:
        print(f"Weather request error {err}")
    return response_weather.json()

def format_current_weather(*, city: str, data: dict):
    result = [f"City/Город: {city}", f"GMT/Часовой пояс: {data['timezone']}", f"shift: {datetime.fromtimestamp(data.get("timezone_offset")).strftime("%H:%M:%S")}"]
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
        if key == "pop":
            result.append(f"Probability of precipitation/Вероятность осадков: {current.get(key) * 100}%")
        if key == "rain":
            result.append(f"Precipitation/Осадки: {current.get(key)} mm/h (мм/ч)")
        result.append(f"{key}: {current.get(key)}")
    return "\n".join(result)

def format_daily_forecast(*, city: str, data:dict, day: int):
    forecast = [f"City/Город: {city}", f"GMT/Часовой пояс: {data['timezone']}", f"shift: {datetime.fromtimestamp(data.get("timezone_offset")).strftime("%H:%M:%S")}",f"Day {day+1}"]
    daily = data["daily"][day]
    if isinstance(daily, dict):
        for k,v in daily.items():
            if k == "dt":
                forecast.append(f"date time: {datetime.fromtimestamp(daily.get(k))}")
                continue
            if k in ("sunrise", "sunset", "moonset", "moonrise"):
                forecast.append(f"{k}: {datetime.fromtimestamp(daily.get(k))}")
                continue
            if k == "summary":
                forecast.append(f"{k}: {v}")
                continue
            if k == "weather":
                forecast.append(f"{k}: {daily.get(k)[0].get("description")} / {daily.get(k)[0].get("main")}")
                continue
            if k == "pop":
                forecast.append(f"Probability of precipitation: {v * 100}%")
            if k == "rain":
                forecast.append(f"Precipitation/Осадки: {v} mm/h (мм/ч)")

            if isinstance(v, dict):
                forecast.append(f"{k}:")
                for k_, v_ in v.items():
                    forecast.append(f"  {k_}: {v_}")
                continue

            forecast.append(f"{k}: {v}")

    return "\n".join(forecast)

def format_hourly_forecast(*, city: str, data: dict, customer_input: str):
    forecast = [f"City/Город: {city}", f"GMT/Часовой пояс: {data['timezone']}", f"shift: {datetime.fromtimestamp(data.get("timezone_offset")).strftime("%H:%M:%S")}"]
    period = list(filter(lambda x: x.isdigit(), customer_input))
    for h in range(int(period[0]) - 1, int(period[1])):
        hours = data.get("hourly")[h]
        forecast.append(f"Hour {h+1}:")
        for k,v in hours.items():
            if k == "dt":
                forecast.append(f"date time: {datetime.fromtimestamp(hours.get(k))}")
                continue
            if k in ("sunrise", "sunset", "moonset", "moonrise"):
                forecast.append(f"{k}: {datetime.fromtimestamp(hours.get(k))}")
                continue
            if k == "summary":
                forecast.append(f"{k}: {v}")
                continue
            if k == "weather":
                forecast.append(f"{k}: {hours.get(k)[0].get("description")} / {hours.get(k)[0].get("main")}")
                continue
            if k == "pop":
                forecast.append(f"Probability of precipitation/Вероятность осадков: {v * 100}%")
                continue
            if k == "rain":
                forecast.append(f"Precipitation/Осадки: {v.get("1h")} mm/h (мм/ч)")
                continue
            forecast.append(f"{k}: {v}")
        forecast.append("\n")

    return "\n".join(forecast)
