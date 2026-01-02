import speech_recognition as sr
from datetime import datetime
import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak Now...")
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio)
            print(f"✅ You said: {command.lower()}")
            return command.lower()
        
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Error: {e}")
        

    return ""



def respond_to_command(command):
    if "hello" in command:
        speak("Hi There!")
    elif "your name" in command:
        speak("My name is Jarvis")
    elif "time" in command:
        current_time = datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
    
    else:
        print("I'm sorry, I don't understand.")
    return True



def main():
    speak("Voice Assistant Activated ✅ ")

    while True:
        command = get_audio()
        if command and not respond_to_command(command):
            break


if __name__ == "__main__":
    main()