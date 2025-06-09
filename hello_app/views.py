from datetime import datetime
from flask import Flask, render_template
from . import app
import requests

@app.route("/")
def home():
    import requests
    api_url = "https://historical-forecast-api.open-meteo.com/v1/forecast?latitude=51.0149&longitude=-3.1029&start_date=2022-12-20&end_date=2022-12-31&hourly=temperature_2m,rain"  # Replace with your API URL
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