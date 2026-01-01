import queue
import sounddevice as sd
from vosk import Model , KaldiRecognizer
import pyttsx3
import json
import datetime


model = Model("model")

recognizer = KaldiRecognizer(model, 16000)

audio_queue = queue.Queue()

tts_engine = pyttsx3.init()

def callback(indata,frames,times,status):
    if status:
        print(status)
    
    audio_queue.put(bytes(indata))

def process_query(query):
    query = query.lower()
    if "time" in query:
        