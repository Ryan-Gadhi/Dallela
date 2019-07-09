from recorder import record
import speech_recognition as sr
from playsound import playsound
import threading
import time
import re
import AudioUtils
i=0
class TriggerWord:

    def __init__(self):
        self.wakeUpWordRecognized = False
        self.threads = []
        self.first_iter = True


    def recognize(self,):
        if self.first_iter:
            self.first_iter = False
        else:
            time.sleep(1)
            #print('sleept')

        audio_txt = None
        record('output.wav')
        r = sr.Recognizer()
        file = sr.AudioFile('output.wav')
        with file as source:
            # global wakeUpWordRecognized
            if not self.wakeUpWordRecognized:
                audio = r.record(source)

                t = threading.Thread(target=self.recognize)
                t.start()
                self.threads.append(t)

                try:
                    audio_txt = r.recognize_google(audio)
                    #print(audio_txt)
                    if self.is_in_wake_words(audio_txt):
                        self.wakeUpWordRecognized = True
                        print('recognized')
                        # playsound('beep.wav')
                        return True
                except Exception :
                    print(' - NOT RECOGNIZED - ')

    def is_in_wake_words(self,text):

        modified = re.search("(\w+)(e|i)(\w+)(a$)", text)
        if modified is not None:
            return True  # add deliver, delhi and driver file and combine with the old file
        elif AudioUtils.is_in_wake_wordsV1(text):
            return True

        return False

    def is_awake(self):
        return self.wakeUpWordRecognized

    def threads_life(self):
        for t in self.threads:
            print(t.isAlive)

    def number_alive(self):
        counter = 0
        for t in self.threads:
            if t.isAlive:
                counter+=1
        return counter

        return counter
    def manage_life(self):
        counter = 0
        for t in self.threads:
            if t.isAlive:
                counter+=1
            else:
                print('is dead')
                self.threads.remove(t)

        return counter

# t = TriggerWord()
# t.recognize()
# time.sleep(10)  # speak about something then before 10 sec say Daleela
# print(is_awake())
