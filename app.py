from flask import Flask, render_template,request
import requests
from datetime import datetime

app=Flask(__name__)

@app.route('/')
def homepage():
    return render_template("index.html")

@app.route('/weatherapp', methods=['POST'])
def get_weatherdata():
    url = "https://api.openweathermap.org/data/2.5/weather"
    param = {
        'q': request.form.get("city"),
        'units': request.form.get("units"),
        #'appid': request.form.get("appid")
        'appid': "0479dcbb42bc93c0d66d43cf9f27acc7"
    }
    response = requests.get(url, params=param)

    if response.status_code != 200:
        error_msg = response.json().get('message', 'Failed to fetch weather data')
        return render_template("index.html", error=error_msg)

    data = response.json()

    # Convert Unix timestamps to human-readable strings
    data['sys']['sunrise'] = datetime.utcfromtimestamp(
        data['sys']['sunrise']
    ).strftime('%Y-%m-%d %H:%M:%S')
    data['sys']['sunset'] = datetime.utcfromtimestamp(
        data['sys']['sunset']
    ).strftime('%Y-%m-%d %H:%M:%S')

    #return f"data: {data}"
    return render_template("weather.html", data=data)

if __name__=='__main__':
    app.run(host="0.0.0.0",port=5002)