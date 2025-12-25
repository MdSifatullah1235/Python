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

stop__event = threading.Event()

def wait_for_enter():
    input("Press Enter to stop recording...")
    stop__event.set()

    