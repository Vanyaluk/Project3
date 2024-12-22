from flask import Flask, render_template, request
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go
import folium
from API import get_location_key, get_weather_data
from manager import check_bad_weather

# Flask App Setup
flask_app = Flask(__name__)

# Dash App Setup
app = Dash(__name__, server=flask_app, url_base_pathname='/dashboard/')

# Dash Layout
app.layout = html.Div([
    html.H1("Визуализация погодных данных"),
    dcc.Dropdown(
        id='city-selector',
        options=[],  # Заполняется динамически
        placeholder="Выберите город"
    ),
    dcc.Graph(id='weather-graph')
])



@flask_app.route('/', methods=['GET', 'POST'])
def index():
    weather_results = []
    error_message = None
    if request.method == 'POST':
        try:
            points = request.form.getlist('points')
            days = int(request.form.get('days', 1))
            if len(points) < 2:
                error_message = "Укажите хотя бы начальную и конечную точки маршрута."
            else:
                for point in points:
                    location_key = get_location_key(point)
                    weather_data = get_weather_data(location_key, days=days)
                    weather_results.append({
                        "city": point,
                        "forecast": weather_data
                    })
        except Exception as e:
            error_message = str(e)

    return render_template('index.html', weather_results=weather_results, error_message=error_message)



@flask_app.route('/map', methods=['POST'])
def map_view():
    try:
        points = request.form.getlist('points')
        if not points:
            return render_template('map.html', error_message="Не указаны точки маршрута.")

        route_map = folium.Map(location=[55.7558, 37.6173], zoom_start=6)

        for point in points:
            location_key = get_location_key(point)
            weather_data = get_weather_data(location_key, days=1)  # Используем 1 день как пример
            lat, lon = [55.7558, 37.6173]  # Здесь добавьте реальные координаты точки
            folium.Marker(
                [lat, lon],
                popup=f"{point}: {weather_data[0]['temperature_max']}°C, {weather_data[0]['rain_probability']}% дождя"
            ).add_to(route_map)

        route_map.save('templates/map.html')
        return render_template('map.html')

    except Exception as e:
        return render_template('map.html', error_message=str(e))

if __name__ == '__main__':
    flask_app.run(debug=True)
