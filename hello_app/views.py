from datetime import datetime
from flask import Flask, render_template
from . import app
import requests

from flask import request

def structure_daily_data(data):
    daily = data['daily']
    keys = daily.keys()
    num_days = len(daily['time'])
    structured = [
        {key: daily[key][i] for key in keys}
        for i in range(num_days)
    ]
    return structured

def get_lat_lon(city):
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    geo_response = requests.get(geo_url)
    geo_data = geo_response.json()
    if geo_data.get('results'):
        lat = geo_data['results'][0]['latitude']
        lon = geo_data['results'][0]['longitude']
        return lat, lon
    return 51.5, -0.12

@app.route("/", methods=["GET"])
def home():
    city=request.args.get("city","London")
    latitude, longitude = get_lat_lon(city)
    start_date = request.args.get("start_date", "2025-03-01")
    end_date = request.args.get("end_date", "2025-04-01")
    api_url = (
        f"https://historical-forecast-api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        f"&start_date={start_date}&end_date={end_date}"
        f"&daily=temperature_2m_max,temperature_2m_min,wind_speed_10m_max,rain_sum,sunrise,sunset"
    )
    response = requests.get(api_url)
    data = response.json()
    daily_data = structure_daily_data(data)
    return render_template('home.html', api_data=daily_data)
    

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")