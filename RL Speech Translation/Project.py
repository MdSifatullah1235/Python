import speech_recognition as sr
import pyttsx3
from googletrans import Translator

def speak(text, language="en"):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    voices = engine.getProperty("voices")

    if language == "en":
        engine.setProperty("voice", voices[0].id)
    else:
        engine.setProperty("voice", voices[1].id if len(voices) > 1 else voices[0].id)

    engine.say(text)
    engine.runAndWait()

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio, language="en-US")
        print(f"You said: {text}")
        return text
    except Exception as e:
        print("Could not understand or connection error.")
        return ""

def translate_text(text, target_language="es"):
    try:
        translator = Translator()
        translation = translator.translate(text, dest=target_language)
        print(f"Translation: {translation.text}")
        return translation.text
    except Exception as e:
        print(f"Translation Error: {e}")
        return ""

def display_language_options():
    print("\n--- Select Language ---")
    print("1. Hindi (hi)\n2. Spanish (es)\n3. French (fr)\n4. German (de)\n5. Japanese (ja)\n6. Bengali (bn)")
    
    choice = input("Enter choice (1-6): ")
    language_dict = {"1":"hi", "2":"es", "3":"fr", "4":"de", "5":"ja", "6":"bn"}
    return language_dict.get(choice, "es")

def main():
    target_language = display_language_options()
    original_text = speech_to_text()

    if original_text:
        translated_text = translate_text(original_text, target_language=target_language)
        if translated_text:
            speak(translated_text, language=target_language)
            print("Done!")

if __name__ == "__main__":
    main()