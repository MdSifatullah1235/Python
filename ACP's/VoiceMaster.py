import pyttsx3
import random

engine = pyttsx3.init()

def get_samples():
    return [
        "Hello, how can I help you today?",
        "The weather is lovely for coding.",
        "To be or not to be, that is the question.",
        "Python is a versatile programming language.",
        "Artificial intelligence is changing the world.",
        "Would you like to hear a story?",
        "Space is the final frontier.",
        "I am learning how to speak better every day.",
        "Coding is like solving a puzzle.",
        "Let's create something amazing together."
    ]

def speak(text):
    engine.say(text)
    engine.runAndWait()

def run_voice_master():
    jokes = [
        "Why did the programmer quit his job? Because he didn't get arrays.",
        "Why do programmers prefer dark mode? Because light attracts bugs.",
        "How many programmers does it take to change a light bulb? None, that's a hardware problem."
    ]
    
    while True:
        command = input("Enter command: ").lower()
        
        if command == "exit":
            break
            
        elif "speed up" in command:
            rate = engine.getProperty('rate')
            engine.setProperty('rate', rate + 50)
            speak("Increasing speed")
            
        elif "slow down" in command:
            rate = engine.getProperty('rate')
            engine.setProperty('rate', rate - 50)
            speak("Slowing down")
            
        elif "increase volume" in command:
            volume = engine.getProperty('volume')
            engine.setProperty('volume', min(1.0, volume + 0.2))
            speak("Increasing volume")
            
        elif "decrease volume" in command:
            volume = engine.getProperty('volume')
            engine.setProperty('volume', max(0.0, volume - 0.2))
            speak("Decreasing volume")
            
        elif "tell a joke" in command:
            speak(random.choice(jokes))
            
        elif "sample" in command:
            speak(random.choice(get_samples()))
            
        else:
            speak("I didn't quite catch that. Try again!")

if __name__ == "__main__":
    run_voice_master()