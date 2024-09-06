import requests
import os

weather_api_key = os.getenv('WEATHER_API_KEY')

def get_weather_data(city):
    
    url = f"https://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}&aqi=no"
    response = requests.get(url)
    data = response.json()
        
    return {
        'temperature': data['current']['temp_c'],
        'humidity': data['current']['humidity'],
        'wind_speed': data['current']['wind_kph'],
        'percipitation': data['current']['precip_mm'],
    }