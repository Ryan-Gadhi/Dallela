import pyttsx3
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.say('hey i am daleela, your voice assistant')
engine.runAndWait()