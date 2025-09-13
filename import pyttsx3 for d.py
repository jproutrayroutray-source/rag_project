import pyttsx3
import random

# Initialize text-to-speech engine
engine = pyttsx3.init()

# List of random love quotes
love_quotes = [
    "You are the love of my life and the reason I smile.",
    "Every love story is beautiful, but ours is my favorite.",
    "I love you not because of who you are, but because of who I am when I am with you.",
    "You are my today and all of my tomorrows.",
    "To love and be loved is to feel the sun from both sides."
]

while True:
    # Take user input
    user_input = input("Say something: ").strip().lower()

    # If user says 'hii', respond with a random love quote
    if user_input == "hii":
        quote = random.choice(love_quotes)
        print(f"💖 {quote}")  # Print the quote
        engine.say(quote)  # Speak the quote
        engine.runAndWait()
