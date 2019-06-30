import speech_recognition as sr
from playsound import playsound
import threading
import time

t1 = None

def speach():

    global start_listening_text
    start_listening_text = None

    r = sr.Recognizer()

    with sr.Microphone() as source:
        try:
            # print("I am listening :")
            # playsound('beep.wav')
            inputAudio = r.listen(source)
            # print("I am sending to google")
            # playsound('beep2.wav')
            threading.Thread(target=speach).start()
            start_listening_text = r.recognize_google(inputAudio)
            print(start_listening_text)

        except:
            print("not recognized by the API :\n")
            start_listening_text = 'Error_001'

t1 = threading.Thread(target=speach)
t1.start()

