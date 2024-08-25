import requests


def get_weather(city, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    complete_url = f"{base_url}?q={city}&appid={api_key}&units=metric"
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
        return "city not found"


def speak_weather():
    city = "London"
    api_key = "YOUR_API_KEY_HERE"
    weather_info = get_weather(city, api_key)
    print(weather_info)
    return weather_info

