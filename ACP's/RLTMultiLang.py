import speech_recognition as sr
from googletrans import Translator, LANGUAGES
import pyttsx3

def translate_speech():
    recognizer = sr.Recognizer()
    translator = Translator()
    engine = pyttsx3.init()

    lang_list = list(LANGUAGES.items())
    print("Available Languages:")
    for i, (code, name) in enumerate(lang_list[:20]):
        print(f"{i}. {name} ({code})")

    try:
        src_idx = int(input("Select Source Language Index (or -1 for Auto-detect): "))
        dest_idx = int(input("Select Target Language Index: "))
        
        src_lang = lang_list[src_idx][0] if src_idx != -1 else None
        dest_lang = lang_list[dest_idx][0]

        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Speaking...")
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language=src_lang if src_lang else 'en-US')
            print(f"Recognized: {text}")

            translation = translator.translate(text, dest=dest_lang)
            print(f"Translated ({translation.src} -> {dest_lang}): {translation.text}")

            engine.say(translation.text)
            engine.runAndWait()

        except sr.UnknownValueError:
            print("Speech unclear. Please try again.")
            translate_speech()
        except sr.RequestError:
            print("Service unavailable.")

    except (ValueError, IndexError):
        print("Invalid selection.")

if __name__ == "__main__":
    translate_speech()