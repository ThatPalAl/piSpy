def get_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "What do you call fake spaghetti? An impasta!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!"
    ]
    return np.random.choice(jokes)

def joke_or_fact():
    speak("Would you like to hear a joke or a fun fact?")
    command = listen_command().lower()
    if "joke" in command:
        joke = get_joke()
        speak(joke)
    elif "fact" in command:
        fact = "Did you know? Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible."
        speak(fact)
    else:
        speak("I didn't understand that. I'll tell you a joke instead.")
        joke = get_joke()
        speak(joke)
    display_menu()