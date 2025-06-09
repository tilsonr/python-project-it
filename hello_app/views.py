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

@app.route("/", methods=["GET"])
def home():
    latitude = request.args.get("latitude", "52.52")
    longitude = request.args.get("longitude", "13.41")
    start_date = request.args.get("start_date", "2025-03-01")
    end_date = request.args.get("end_date", "2025-04-01")
    api_url = (
        f"https://historical-forecast-api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        f"&start_date={start_date}&end_date={end_date}"
        f"&daily=temperature_2m_max,temperature_2m_min,wind_speed_10m_max,rain_sum"
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