import threading
import time
import os
import sys
import time
import pyaudio
import wave 
import SpeechRecognition as sr
import numpy as np
import matplotlib.pyplot as plt
from speech_recognition import AudioData
from colorama import init,Fore,Style

init(autoseret=True)

stop_event = threading.Event()

def wait_for_enter():

    print(f"{Fore.YELLOW}Press enter to stop recording")
    stop_event.set()

def spinner():
    spinner_chars = "/-\|"
    idx = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r{spinner_chars[idx]}")
        sys.stdout.flush()
        idx = idx + 1

        time.sleep(0.1)
    sys.stdout.write("\r Recording Stopped ! \n")

        
def record_untill_enter():
    p = pyaudio.PyAudio()
    format = pyaudio.paInt16
    channels = 1
    rate = 16000
    frames_per_buffer = 1024


    stream = p.open(format=format, channels=channels,rate=rate,input=True,frames_per_buffer=frames_per_buffer)
    frames = []

    threading.Thread(target=wait_for_enter()).start()
    threading.Thread(target=spinner).start()

    while not stop_event.is_set():
        try:
            data = stream.read(frames_per_buffer)
            frames.append(data)

        except Exception as e:
            print(f"{Fore.RED}Error: {e}")
            break
    
    stream.stop_stream()
    stream.close()
    sample_width = p.get_sample_size(format)
    p.terminate()
    audio_date = b"".join(frames)
    return audio_data,rate,sample_width

def save_audio(data,rate,sample_width,file_name="audio.wav"):
    with wave.open(file_name,"wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(data)
    
    print(f"{Fore.GREEN}Audio saved to {file_name}")


def transcribe_audio(data,rate,sample_width,file_name="transcription.txt"):
    r = sr.recognizer()
    audio = AudioData(data,rate,sample_width)
    try:
        text = r.recognize_google(audio)
    
    except Exception as e:
        text = f"{Fore.RED}Could not transcribe audio"
    
    except sr.RequestError as e:
        text = f"{Fore.RED}Could not request results from Google Speech Recognition service; {e}"
    

    print("Transcription:",text)
    with open(file_name,"w") as f:
        f.write(text)

    print(f"{Fore.GREEN}Transcription saved to {file_name}")


def show_waveform(data,rate,sample_width):
    samples = np.frombuffer(data,dtype=np.int16)
    time_axis = np.linspace(0,len(samples)/rate,len(samples))
    plt.plot(time_axis,samples)
    plt.title("Waveform")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    plt.show()


def main():
    print("Start Speaking press enter to stop")
    audio_data,rate,sample_width = record_untill_enter()
    save_audio(audio_data,rate,sample_width)
    transcribe_audio(audio_data,rate,sample_width)
    show_waveform(audio_data,rate,sample_width)

if __name__ == "__main__":
    main()