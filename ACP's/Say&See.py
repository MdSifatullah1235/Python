import threading
import time
import sys
import pyaudio
import wave 
import speech_recognition as sr
import numpy as np
import matplotlib.pyplot as plt
from speech_recognition import AudioData

stop_event = threading.Event()

def wait_for_enter():
    input()
    stop_event.set()

def spinner():
    spinner_chars = "|/-\\"
    idx = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r{spinner_chars[idx % 4]} Recording... Press Enter to Stop")
        sys.stdout.flush()
        idx += 1
        time.sleep(0.1)
    sys.stdout.write("\r Recording Stopped!            \n")

def record_until_enter():
    stop_event.clear()
    
    p = pyaudio.PyAudio()
    audio_format = pyaudio.paInt16
    channels = 1
    rate = 16000
    frames_per_buffer = 1024


    stream = p.open(format=audio_format, channels=channels, rate=rate, 
                    input=True, frames_per_buffer=frames_per_buffer)
    frames = []

    threading.Thread(target=wait_for_enter, daemon=True).start()
    threading.Thread(target=spinner, daemon=True).start()

    while not stop_event.is_set():
        try:
            data = stream.read(frames_per_buffer, exception_on_overflow=False)
            frames.append(data)
        except Exception as e:
            print(f"Error during recording: {e}")
            break

    stream.stop_stream()
    stream.close()
    sample_width = p.get_sample_size(audio_format)
    p.terminate()

    audio_data = b"".join(frames)
    return audio_data, rate, sample_width

def save_audio(data, rate, width, file_name="speech.wav"):
    with wave.open(file_name, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(width)
        wf.setframerate(rate)
        wf.writeframes(data)
    print(f"Audio saved to {file_name}")

def audio_transcribe(data, rate, width, file_name="speech.txt"):
    r = sr.Recognizer()
    audio = AudioData(data, rate, width)
    print("Transcribing...")
    try:
        text = r.recognize_google(audio)
    except sr.UnknownValueError:
        text = "[Could not understand audio]"
    except sr.RequestError as e:
        text = f"[API Error: {e}]"
    
    print(f"Transcription: {text}")
    with open(file_name, "w") as f:
        f.write(text)
    print(f"Transcription saved to {file_name}")

def show_waveform(data, rate):
    samples = np.frombuffer(data, dtype=np.int16)
    time_axis = np.linspace(0, len(samples) / rate, num=len(samples))
    
    plt.figure(figsize=(10, 4))
    plt.plot(time_axis, samples, color="blue")
    plt.title("Audio Waveform")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    print("--- Voice Recorder & Transcriber ---")
    print("Press Enter to start and stop.")
    
    audio_data, rate, width = record_until_enter()
    
    if audio_data:
        save_audio(audio_data, rate, width)
        audio_transcribe(audio_data, rate, width)
        show_waveform(audio_data, rate)
    else:
        print("No audio captured.")

if __name__ == "__main__":
    main()