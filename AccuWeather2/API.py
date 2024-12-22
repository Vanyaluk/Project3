import requests

API_KEY = "Pww3hKucqZjMK9Y1dOKLwxciaRJbipdq"
BASE_LOCATION_URL = "http://dataservice.accuweather.com/locations/v1/cities/search"
BASE_FORECAST_URL = "http://dataservice.accuweather.com/forecasts/v1/daily/1day/"


def get_location_key(city):
    try:
        params = {"apikey": API_KEY, "q": city}
        response = requests.get(BASE_LOCATION_URL, params=params, timeout=5)

        if response.status_code != 200 or not response.json():
            raise ValueError(f"Город {city} не найден")

        return response.json()[0]["Key"]
    except requests.exceptions.Timeout:
        raise Exception("Превышено время ожидания ответа от сервера.")
    except requests.exceptions.ConnectionError:
        raise Exception("Ошибка подключения. Проверьте интернет-соединение.")
    except Exception as e:
        raise Exception(f"Ошибка при поиске города: {e}")


def get_weather_data(location_key):
    try:
        params = {"apikey": API_KEY, "metric": True}
        response = requests.get(f"{BASE_FORECAST_URL}{location_key}", params=params, timeout=5)

        if response.status_code != 200:
            raise ValueError("Ошибка получения прогноза погоды!")

        forecast = response.json().get("DailyForecasts", [{}])[0]
        temperature = forecast.get("Temperature", {}).get("Maximum", {}).get("Value", "Нет данных")
        wind_speed = forecast.get("Day", {}).get("Wind", {}).get("Speed", {}).get("Value", "Нет данных")
        rain_probability = forecast.get("Day", {}).get("PrecipitationProbability", "Нет данных")

        return temperature, wind_speed, rain_probability
    except requests.exceptions.Timeout:
        raise Exception("Превышено время ожидания ответа от сервера.")
    except requests.exceptions.ConnectionError:
        raise Exception("Ошибка подключения. Проверьте интернет-соединение.")
    except Exception as e:
        raise Exception(f"Ошибка обработки данных прогноза: {e}")

