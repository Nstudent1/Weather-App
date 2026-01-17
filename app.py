from flask import Flask, render_template, request
from dotenv import load_dotenv

import requests
import os

load_dotenv()

api_key = os.getenv("OPENWEATHER_API_KEY")

if not api_key:
    raise ValueError("API key not found. Check your .env file.")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city_name = request.form.get("city-name").strip()

        if city_name == "":
            error = "City name cannot be empty"
            return render_template("index.html", error=error)
        
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        full_url = base_url + "?q=" + city_name + "&appid=" + api_key + "&units=imperial"

        response = requests.get(full_url)
        weather_data = response.json()

        if int(weather_data.get("cod")) == 404:
            error = "City not found"
            return render_template("index.html", error=error)
        elif int(weather_data.get("cod")) == 401:
            raise ValueError("Invalid API key")
        elif int(weather_data.get("cod")) != 200:
            raise ValueError("An error occurred while fetching the weather data")
        
        temperature = weather_data["main"].get("temp", "N/A") # "N/A" if missing
        humidity = weather_data["main"].get("humidity", "N/A")
        wind_speed = weather_data["wind"].get("speed", "N/A")

        if "weather" in weather_data and len(weather_data["weather"]) > 0:
            weather_description = weather_data["weather"][0].get("description", "N/A")
        else:
            weather_description ="N/A"

        return render_template("index.html", city_name=city_name, temp=temperature, humidity=humidity, wind_speed=wind_speed, weather_description=weather_description)
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
