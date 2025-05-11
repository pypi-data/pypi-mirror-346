import requests

class WeatherFetcher:
    def __init__(self, api_url="https://api.theanon.xyz/weather"):
        self.api_url = api_url

    def get_weather(self, city):
        response = requests.get(self.api_url, params={"city": city})
        data = response.json()

        if response.status_code != 200:
            raise Exception(data.get("error", "Failed to fetch weather"))

        return data
