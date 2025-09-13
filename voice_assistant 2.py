import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()

engine.setProperty('rate', 150)  
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(" Listening... Speak now!")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5) 
            command = recognizer.recognize_google(audio)  
            command = command.lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Could not understand the audio")
            return None
        except sr.RequestError:
            print(" Could not request results, check internet connection")
            return None
        except sr.WaitTimeoutError:
            print(" You didn't say anything!")
            return None
while True:
    command = take_command()
    if command:
        if "hello deepshikha" in command or "hi deepshikha" in command:
            speak("Hello! How can I assist you my love?")
        elif "how are you deepshikha" in command:
            speak("don't annoy me, but I'm doing great! How about you?")
        elif "exit" in command or "bye" in command:
            speak("Goodbye! Have a great day!")
            break
        else:
            speak("I didn't understand that, but I'm learning!")
