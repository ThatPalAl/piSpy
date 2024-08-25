import time

def set_reminder():
    speak("Please tell me the reminder and the time to remind you. For example, 'Remind me to take a break in 10 seconds'.")
    command = listen_command().lower()
    if "seconds" in command:
        seconds = int(command.split("in")[1].strip().split()[0])
        reminder_text = command.split("remind me to")[1].split("in")[0].strip()
        speak(f"Setting a reminder to {reminder_text} in {seconds} seconds.")
        time.sleep(seconds)
        speak(f"Reminder: {reminder_text}")
    elif "minutes" in command:
        minutes = int(command.split("in")[1].strip().split()[0])
        reminder_text = command.split("remind me to")[1].split("in")[0].strip()
        speak(f"Setting a reminder to {reminder_text} in {minutes} minutes.")
        time.sleep(minutes * 60)
        speak(f"Reminder: {reminder_text}")
    else:
        speak("I didn't understand the time frame. Please try again.")
        set_reminder()
    display_menu()
