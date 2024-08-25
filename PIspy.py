import tkinter as tk
from threading import Thread
import speech_recognition as sr
from gtts import gTTS
import openai
import os
import sys
import pygame
import requests
import googlemaps
from datetime import datetime
import wikipediaapi

from piSpy.reminder import set_reminder
from projekt.piSpy.wiki import Weather
from piSpy.joke import get_joke, joke_or_fact

sys.stderr = open(os.devnull, 'w')

pygame.mixer.init()

r = sr.Recognizer()

gmaps = googlemaps.Client(key='')

openai.api_key = ""

news_api_key = ""

weather_api_key = ""

weather_instance = Weather(weather_api_key)

def listen_command():
    with sr.Microphone() as source:
        print('Listening...')
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio)
        print('You said: ' + command)
        return command
    except sr.UnknownValueError:
        return "I couldn't understand the audio"
    except sr.RequestError as e:
        return "Could not request results; {0}".format(e)


def speak(text):
    print("Response text:", text)
    language = 'en'
    tts = gTTS(text=text, lang=language)
    tts.save("response.mp3")
    pygame.mixer.music.load("response.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def get_weather(city):
    return weather_instance.speak_weather(city)


def get_news(api_key):
    api_url = "https://newsapi.org/v2/top-headlines"
    params = {'country': 'us',
              'apiKey': api_key
              }
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        news_data = response.json()
        news_report = ""
        for article in news_data['articles'][:5]:
            title = article['title']
            description = article.get('description', 'no description available')
            if 'removed' in title.lower():
                continue
            news_report += f"Title: {title} \nDescription: {description}\n\n"

        return news_report
    else:
        return f"Error : {response.status_code}"


def get_recipe(ingredients):
    prompt = f"Provide a recipe based on these ingredients: {', '.join(ingredients)}."
    response = chat_with_gpt(prompt)
    return response


def chat_with_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


def get_daily_history():
    curr_date = datetime.now()
    curr_day = curr_date.day
    curr_month = curr_date.month

    wiki = wikipediaapi.Wikipedia(language='en',
                                  user_agent='DailyHistory/1.0 (https://example.com; contact@example.com)')

    query = f"https://en.wikipedia.org/w/index.php?title=Wikipedia:Selected_anniversaries/{curr_date.strftime('%B')}_{curr_day}"
    page = wiki.page(query)

    if page.exists():
        return page.text
    else:
        return "No historical events found for today."


def display_menu():
    menu_options = """Main Menu:
    1. Speak with GPT
    2. Recipe
    3. Weather
    4. News for today
    5. Daily History
    6. Tell me a joke or fun fact
    7. Set a reminder
    8. Exit"""
    
    speak(menu_options)
    menu_label.config(text=menu_options)
    root.after(5000, listen_for_menu_option)


def listen_for_menu_option():
    command = listen_command()
    if "speak with gpt" in command.lower() or command.strip() == "1":
        speak("You chose to speak with GPT. Please start talking.")
        conversation()
    elif "recipe" in command.lower() or command.strip() == "2":
        speak("Please list the ingredients you have.")
        recipe()
    elif "weather" in command.lower() or command.strip() == "3":
        speak("Please say the city name for the weather.")
        weather()
    elif "news for today" in command.lower() or command.strip() == "4":
        speak("Fetching news for today.")
        news()
    elif "daily history" in command.lower() or command.strip() == "5":
        speak("Fetching historical events for today.")
        daily_history()
    elif "tell me a joke or fun fact" in command.lower() or command.strip() == "6":
        joke_or_fact()
    elif "set a reminder" in command.lower() or command.strip() == "7":
        set_reminder()
    elif "exit" in command.lower() or command.strip() == "7":
        speak("Goodbye!")
        root.quit()
        
    else:
        speak("Invalid option. Please try again.")
        display_menu()


def conversation():
    command = listen_command()
    response = chat_with_gpt(command)
    speak(response)
    display_menu()


def recipe():
    ingredients = listen_command().split(", ")
    recipe = get_recipe(ingredients)
    speak(recipe)
    display_menu()


def weather():
    city = listen_command()
    weather_report = get_weather(city)
    speak(weather_report)
    display_menu()


def news():
    news_report = get_news(news_api_key)
    speak(news_report)
    display_menu()


def daily_history():
    history_report = get_daily_history()
    speak(history_report)
    display_menu()


root = tk.Tk()
root.title("AI Assistant")

menu_label = tk.Label(root, text="", font=("Helvetica", 16))
menu_label.pack(pady=20)

start_button = tk.Button(root, text="Start", command=display_menu, font=("Helvetica", 14))
start_button.pack(pady=20)

root.mainloop()
