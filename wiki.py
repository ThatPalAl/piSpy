import requests

class Weather:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_weather(self, city):
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        complete_url = f"{base_url}?q={city}&appid={self.api_key}&units=metric"
        response = requests.get(complete_url)
        weather_data = response.json()

        if weather_data["cod"] != 404:
            main = weather_data['main']
            temperature = main['temp']
            humidity = main['humidity']
            weather_description = weather_data['weather'][0]['description']
            weather_report = (f"Temperature: {temperature} degrees\n"
                              f"Humidity: {humidity} % \n"
                              f"description: {weather_description.capitalize()}.")

            return weather_report
        else:
            return "City not found"

    def speak_weather(self, city):
        weather_info = self.get_weather(city)
        return weather_info
