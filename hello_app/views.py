from datetime import datetime
from flask import Flask, render_template
from . import app
import requests

@app.route("/")
def home():
    import requests
    api_url = "https://historical-forecast-api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&start_date=2025-03-01&end_date=2025-04-01&hourly=temperature_2m,rain" 
    response = requests.get(api_url)
    data = response.json()  # Adjust as needed for your API's response
    return render_template('home.html', api_data=data)
    

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