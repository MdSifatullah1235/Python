import pyttsx3
import speech_recognition as sr
from datetime import datetime
import random

engine = pyttsx3.init()

def facts():
    interesting_facts_list = ["Octopuses actually have 3 hearts","a cloud weighs around a million tonnes","your brain is constantly eating itself","Mars isn't actually round","the fear of long words is called Hippopotomonstrosesquippedaliophobia"]
    return random.choice(interesting_facts_list)



def conversation():
    user_input = input("Enter your command: ")
    if "hello" in user_input:
        print("Hi there!")
    elif "time" in user_input:
        print("The current time is:", datetime.now().strftime("%H:%M:%S"))

    elif "fact" in user_input:
        engine.say(facts())
        engine.runAndWait()
    elif "use male voice" in user_input:
        engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
    elif "use female voice" in user_input:
        engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0')
    
    else:
        print("I'm sorry, I don't understand.")