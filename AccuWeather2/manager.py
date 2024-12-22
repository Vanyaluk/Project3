# Проверка неблагоприятных погодных условий
def check_bad_weather(temperature, wind_speed, rain_probability):
    if temperature < 0 or temperature > 35:
        return True
    if wind_speed > 50:
        return True
    if rain_probability > 70:
        return True
    return False