import threading
import time
import os
import sys
import pyaudio
import wave 
import speech_recognition as sr
import numpy as np
import matplotlib.pyplot as plt
from speech_recognition import AudioData
from colorama import init, Fore, Style

init(autoreset=True)

stop_event = threading.Event()

def wait_for_enter():
    input()
    stop_event.set()

def spinner():
    spinner_chars = "/-\|"
    idx = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r{Fore.CYAN}{spinner_chars[idx % 4]} Recording... Press Enter to Stop")
        sys.stdout.flush()
        idx += 1
        time.sleep(0.1)
    sys.stdout.write("\r" + " " * 40 + "\r")
    print(f"{Fore.GREEN}Recording Stopped!")

def record_untill_enter():
    p = pyaudio.PyAudio()
    audio_format = pyaudio.paInt16
    channels = 1
    rate = 16000
    frames_per_buffer = 1024

    stream = p.open(format=audio_format, 
                    channels=channels, 
                    rate=rate, 
                    input=True, 
                    frames_per_buffer=frames_per_buffer)
    
    frames = []

    threading.Thread(target=wait_for_enter, daemon=True).start()
    threading.Thread(target=spinner, daemon=True).start()

    while not stop_event.is_set():
        try:
            data = stream.read(frames_per_buffer, exception_on_overflow=False)
            frames.append(data)
        except Exception as e:
            print(f"{Fore.RED}Error: {e}")
            break
    
    stream.stop_stream()
    stream.close()
    sample_width = p.get_sample_size(audio_format)
    p.terminate()
    
    audio_data = b"".join(frames)
    return audio_data, rate, sample_width

def save_audio(data, rate, sample_width, file_name="audio.wav"):
    with wave.open(file_name, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(data)
    print(f"{Fore.BLUE}Audio saved to {file_name}")

def transcribe_audio(data, rate, sample_width, file_name="transcription.txt"):
    r = sr.Recognizer()
    audio = AudioData(data, rate, sample_width)
    print(f"{Fore.YELLOW}Transcribing...")
    
    try:
        text = r.recognize_google(audio)
    except sr.UnknownValueError:
        text = "[Could not understand audio]"
    except sr.RequestError as e:
        text = f"[API Error: {e}]"
    except Exception as e:
        text = f"[Error: {e}]"

    print(f"{Fore.WHITE}Transcription: {text}")
    with open(file_name, "w") as f:
        f.write(text)
    print(f"{Fore.BLUE}Transcription saved to {file_name}")

def show_waveform(data, rate, sample_width):
    samples = np.frombuffer(data, dtype=np.int16)
    time_axis = np.linspace(0, len(samples) / rate, num=len(samples))
    
    plt.figure(figsize=(10, 4))
    plt.plot(time_axis, samples, color='blue')
    plt.title("Recorded Audio Waveform")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    print(f"{Fore.MAGENTA}--- Voice Recorder & Transcriber ---")
    audio_data, rate, sample_width = record_untill_enter()
    
    if len(audio_data) > 0:
        save_audio(audio_data, rate, sample_width)
        transcribe_audio(audio_data, rate, sample_width)
        show_waveform(audio_data, rate, sample_width)
    else:
        print(f"{Fore.RED}No audio captured.")

if __name__ == "__main__":
    main()