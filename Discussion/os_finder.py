import speech_recognition as sr
from playsound import playsound
import threading
import time


r = sr.Recognizer()

harvard = sr.AudioFile('harvard.wav')
with harvard as source:
   audio = r.record(source,duration=4)
   playsound(audio)