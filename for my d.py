import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import datetime
import time

engine = pyttsx3.init()
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(text):
    print(f"🤖 Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            print(f"🗣 You said: {command}")
            return command
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            speak("Error connecting to the internet.")
            return None
        except sr.WaitTimeoutError:
            return None

def open_application(app_name):
    if "chrome" in app_name:
        speak("Opening Chrome")
        os.system("start chrome")
    elif "notepad" in app_name:
        speak("Opening Notepad")
        os.system("notepad")
    elif "calculator" in app_name:
        speak("Opening Calculator")
        os.system("calc")
    else:
        speak("Sorry, I can't open that app yet.")

def search_google(query):
    speak(f"Searching Google for {query}")
    webbrowser.open(f"https://www.google.com/search?q={query}")

def search_youtube(query):
    speak(f"Searching YouTube for {query}")
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

def set_reminder(reminder_time, reminder_text):
    speak(f"Reminder set for {reminder_time}. I will remind you.")
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        if current_time == reminder_time:
            speak(f"Reminder: {reminder_text}")
            break
        time.sleep(30)

speak("Say 'Hi Deepshikha' to start")
while True:
    command = take_command()
    if command and ("hi deepshikha" in command or "hello deepshikha" in command):
        speak("Hello! How can I assist you my love?")
        break

while True:
    command = take_command()
    
    if command:
        if "how are you deepshikha" in command:
            speak("Don't annoy me, but I'm doing great! How about you?")
        
        elif "open" in command:
            open_application(command.replace("open ", ""))

        elif "search google for" in command:
            search_google(command.replace("search google for ", ""))

        elif "search youtube for" in command:
            search_youtube(command.replace("search youtube for ", ""))

        elif "set reminder for" in command:
            try:
                parts = command.replace("set reminder for ", "").split(" to ")
                reminder_time = parts[0].strip()
                reminder_text = parts[1].strip()
                set_reminder(reminder_time, reminder_text)
            except IndexError:
                speak("Please say the reminder in this format: 'Set reminder for HH:MM to reminder text'")

        elif "exit" in command or "bye" in command:
            speak("Goodbye! Have a great day!")
            break
        
        else:
            speak("I didn't understand that, but I'm learning!")
