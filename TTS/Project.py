import speech_recognition as sr
import pyttsx3
from googletrans import Translator
import asyncio

def speak(text, language="en"):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    voices = engine.getProperty('voices')

    if language == "en":
        engine.setProperty('voice', voices[0].id)
    else:
        engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)

    engine.say(text)
    engine.runAndWait()

def speach_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please speak:")
        recognizer.adjust_for_ambient_noise(source) 
        audio = recognizer.listen(source)

    try:
        print("Recognizing Speech...")
        text = recognizer.recognize_google(audio, language="en-US")
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Error: {e}")
    return None

async def translate_text(text, target_language="es"):
    translator = Translator()
    translation = await translator.translate(text, dest=target_language)
    print(f"Translation: {translation.text}")
    return translation.text

def display_language_options():
    print("Available language options:")
    print("1. English (en) | 2. Spanish (es) | 3. French (fr)")
    print("4. German (de)  | 5. Japanese (ja) | 6. Bengali (bn)")

    choice = input("Enter your choice (1-6): ")
    language_dict = {"1":"en","2":"es","3":"fr","4":"de","5":"ja","6":"bn"}  
    return language_dict.get(choice,"es")

def main():
    target_language = display_language_options()
    original_text = speach_to_text()

    if original_text:
        translated_text = asyncio.run(translate_text(original_text, target_language))
        
        if translated_text:
            speak(translated_text, language=target_language)
            print("Translation Spoken out")

if __name__ == "__main__":
    main()