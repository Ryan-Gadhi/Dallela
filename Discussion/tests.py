from tkinter import *
import pyttsx3
import threading
import speech_recognition as sr

def look_for_trigger():
	print('started')
	r = sr.Recognizer()
	with sr.Microphone() as source:
	    try:
	        print("I am listening :")
	        input_audio = r.listen(source)
	        audio_text = r.recognize_google(input_audio)
	    except :
	        print("not recognized by the API")

	return audio_text

def sound():
	print(look_for_trigger())



root = Tk()
var = StringVar()
var.set('hello')

l = Label(root, textvariable = var)
l.pack()

t = Entry(root, textvariable = var)
t.pack()

x = threading.Thread(target=sound)
x.start()


root.mainloop() #

