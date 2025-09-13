import speech_recognition as sr
import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Set voice properties
engine.setProperty('rate', 150)  # Slows down speech
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Change index to try different voices

# Function to speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to take voice input
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening... Speak now!")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        try:
            audio = recognizer.listen(source, timeout=5)  # Listen for 5 seconds
            command = recognizer.recognize_google(audio)  # Convert speech to text
            command = command.lower()
            print(f"🗣 You said: {command}")
            return command
        except sr.UnknownValueError:
            print("❌ Could not understand the audio")
            return None
        except sr.RequestError:
            print("❌ Could not request results, check internet connection")
            return None
        except sr.WaitTimeoutError:
            print("⏳ You didn't say anything!")
            return None

# Main loop for listening to voice commands
while True:
    command = take_command()
    if command:
        if "hello dp" in command or "hi dp" in command:
            speak("Hello! How can I assist you my love?")
        elif "how are you dp" in command:
            speak("don't annoy me, but I'm doing great! How about you?")
        elif "exit" in command or "bye" in command:
            speak("Goodbye! Have a great day!")
            break
        else:
            speak("I didn't understand that, but I'm learning!")
