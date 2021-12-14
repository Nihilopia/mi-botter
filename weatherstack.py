import os
from requests.api import request
import json

base_url = "api.weatherstack.com"
api_key = os.environ["mibtoken"]

def get_current_weather(city):
    try:
        response = request("GET", f"http://api.weatherstack.com/current?access_key={api_key}&query={city}")
    except Exception as e:
        return json.dumps({"error": str(e)})
    if response.status_code == 200:
        return json.loads(response.text)