import platform
import pyttsx3

'''
notes on this class:
 creating multiple instances uses keeps the same sound configuration
 passing '' to pyttsx3 say() freezes the application (handled here)
 pyttsx3 can't work on multiple threads

'''

class Speaking:

    def __init__(self):
        self.engine = pyttsx3.init()

    def say(self,text):
        if text=='':
            return
        self.engine.say(text)
        self.engine.runAndWait()

    def findOS_Sound(self):
        os_name = platform.system()
        name = 'undefined'
        if os_name == 'Windows':
            name = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'
        elif os_name == 'Darwin':
            name = 'com.apple.speech.synthesis.voice.samantha'
        elif os_name == 'Linux':
            name = 'female3'
        else:
            print('os not recognized')
        return name


    def womanAudio(self):
        name = self.findOS_Sound()
        print(self)
        try:
            self.engine.setProperty('voice', name)
            self.engine.setProperty('rate', 150) 
        except():
            print('specified sound not found in the local system!')
