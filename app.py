import requests
from flask import Flask, jsonify, render_template, render_template_string

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

# Déposez votre code à partir d'ici :

@app.route("/contact")
def MaPremiereAPI():
    return render_template("contact.html")

@app.get("/paris")
def api_paris():
    url = "https://api.open-meteo.com/v1/forecast?latitude=48.8566&longitude=2.3522&hourly=temperature_2m"
    response = requests.get(url)
    data = response.json()

    times = data.get("hourly", {}).get("time", [])
    temps = data.get("hourly", {}).get("temperature_2m", [])

    n = min(len(times), len(temps))
    result = [
        {"datetime": times[i], "temperature_c": temps[i]}
        for i in range(n)
    ]

    return jsonify(result)

@app.route("/rapport")
def mongraphique():
    return render_template("graphique.html")

@app.route("/atelier")
def atelier():
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=43.2965"
        "&longitude=5.3698"
        "&current_weather=true"
        "&timezone=Europe%2FParis"
    )

    response = requests.get(url)
    data = response.json()

    wind_speed = data.get("current_weather", {}).get("windspeed", 0)

    return render_template("atelier.html", wind=wind_speed)

@app.route("/histogramme")
def histogramme():
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=48.8566"
        "&longitude=2.3522"
        "&daily=temperature_2m_max"
        "&timezone=Europe%2FParis"
        "&forecast_days=7"
    )

    response = requests.get(url)
    data = response.json()

    dates = data.get("daily", {}).get("time", [])
    temperatures = data.get("daily", {}).get("temperature_2m_max", [])

    n = min(len(dates), len(temperatures))
    chart_rows = [[dates[i], temperatures[i]] for i in range(n)]

    return render_template("histogramme.html", chart_rows=chart_rows)

# Ne rien mettre après ce commentaire
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)