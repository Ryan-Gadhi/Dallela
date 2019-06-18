from gtts import gTTS
import playsound
import os

tts = gTTS(' ')
tts.save('hello.mp3')

path = os.getcwd()+'/hello.mp3'
playsound.playsound(path, True)