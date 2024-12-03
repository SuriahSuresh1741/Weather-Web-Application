import os
import requests
from flask import Flask, render_template ,request

app=Flask(__name__)

@app.route('/')
def home():
    return render_template("weather_website.html")


@app.route('/process', methods=['POST'])
def search():
    city_name = request.form['cityname'].title()
    API_KEY = os.environ.get("API_KEY")
    WEATHER_API = "https://api.openweathermap.org/data/2.5/weather"
    GEOCODING_API = "http://api.openweathermap.org/geo/1.0/direct"
    Geocode_params = {
        "q": city_name,
        "appid": API_KEY,
    }
    response_geo = requests.get(GEOCODING_API, params=Geocode_params)
    LATITUDE = response_geo.json()[0]["lat"]
    LONGITUDE = response_geo.json()[0]["lon"]

    weather_params = {
        "lat": LATITUDE,
        "lon": LONGITUDE,
        "appid": API_KEY,
        "units": "metric"
    }

    response_weather = requests.get(WEATHER_API, params=weather_params)

    # Details to be used for website
    description = response_weather.json()['weather'][0]['description'].title()
    current_temperature = response_weather.json()["main"]["temp"]
    minimum_temperature = response_weather.json()["main"]["temp_min"]
    maximum_temperature = response_weather.json()["main"]["temp_max"]
    pressure = response_weather.json()["main"]["pressure"]
    humidity = response_weather.json()["main"]["humidity"]
    wind_speed = response_weather.json()["wind"]["speed"]
    return render_template("results.html",
                           description=description,current_temperature=current_temperature,
                           minimum_temperature=minimum_temperature,maximum_temperature=maximum_temperature,
                           pressure=pressure,humidity=humidity,wind_speed=wind_speed,CityName=city_name)



if __name__ == "__main__":
    app.run(debug=True)