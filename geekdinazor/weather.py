import requests
from urllib3.exceptions import HTTPError

def fetch_weather(city):
    api_key = "87cbe19012db96d022e0d11237cdd5f5"
    r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=tr&APPID={api_key}")
    if r.status_code == 200:
        j = r.json()
        return {"status": j["weather"][0]["description"], "temp": j["main"]["temp"], "temp_feels_like": j["main"]["feels_like"]}
    else:
        raise HTTPError(f"API Error from Openweathermap: {r.status_code}")
