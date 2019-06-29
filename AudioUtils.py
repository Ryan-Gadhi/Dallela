import speech_recognition as sr
import pyttsx3
import platform
from playsound import playsound
import threading
import re
from speaking import Speaking
from interpeter.skills.Trvial_Skill import TrivialSkills


global_engine = None
wake_up_text = None
t1 = None

class AudioUtils:

    def __init__(self):
        self.sp = Speaking()
        self.sp.womanAudio()
        self.max_trials = 2  # the number of times the system will listen before sleeping
        self.current_trial = 0
        self.listening_text = None
        self.t1 = None # the listening thread


    def set_trials(self,int):
        self.max_trials = int

    def is_in_wake_wordsv1(audio_text):
        """
            # currently not used

            checks if the audio text is in the file
            containing words similar to Daleela

            this function checks if the word
            said is one of the similar words to
            Dalela in wake_up_words.txt

        """
        print(' should not be used')
        file = open('wake_up_words.txt', 'r')

        similar_words = (file.read().split('\n'))  # making a list
        for word in similar_words:  # going over that list
            if word.lower() in audio_text.lower():
                not_wakeup_word = False
                # print('it matches ' + word)
                return True
        return False

    def get_listening_text(self,):
        return self.listening_text

    def is_in_wake_words(text):
        """
            # this is a temporary method, should be overridden by Tenserflow
            checks if the said word feels sound like Daleela

        """
        text = re.search("(\w+)(e|i)(\w+)(a$)", text)
        if text is not None:
            return True # add deliver and delhi

        return False

    def listening_Helper(self):
        """
            this method:
                        adds the 2 beep sounds
                        connects to google's server
                        for speech recognition

            awake: a boolean value that reflects weather
            the wake word has been said or not
        """
        # if self.current_trial < self.max_trials:

        r = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                print("I am listening :")
                playsound('beep.wav')
                input_audio = r.listen(source)

                print("Connecting .. ")
                playsound('beep2.wav')

                self.listening_text = r.recognize_google(input_audio)

                print("You said : {}".format(self.listening_text))
                # self.current_trial = self.max_trials  # stopping the method from re-executing

            except:
                print(" -- NOT RECOGNIZED -- (In Listening)")
                # self.current_trial += 1
                self.listening_text = 'Error_101'

                # if self.max_trial < curr_trial:
                #     recog_error = 'Error_101'
                #     skill_found, answer = TrivialSkills.search_for_match(recog_error)
                #     if skill_found:
                #         self.sp.say(answer)
                #     else:
                #         print('skill not found')
                #         raise Exception



    def start_listening(self,awake=None,trials=3):
        """
            this method makes a new thread to handle
            google server connection in the background

            awake: a boolean value that reflects weather
            the wake word has been said or not

        """

        self.t1 = threading.Thread(target=self.listening_Helper)
        self.t1.start()
        return self.t1

    # not
    def findOS_Sound(self,):
        """
            the following is only related to pyttsx3 package
            it checks for woman sound in the local system
            and choose as the default

        """
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

    """
        the following is only related to pyttsx3 package
        it checks for woman sound in the local system
        and choose as the default sound output
    
    """

    # not
    def test_audio(self,):
        name = self.findOS_Sound()
        global global_engine
        global_engine = pyttsx3.init()

        try:
            global_engine.setProperty('voice', name)
            print('property has been set..')
        except():
            print('specified sound not found in the local system!')
        return global_engine

        """
            this method is responsible for the sound output
            it is called by 'reply' method to make a new thread
            text: input text to be said
               
        """

    # not
    def replyHelper(text):
        # print('audio')

        engine = global_engine
        print(text+ "<<<<<<<<<")
        engine.say(text)

        engine.runAndWait()

        print(text)

    # not
    def reply(self,text):
        # print('finished audio')
        """
            makes a new thread that handles the sound output
            in a new thread

            text: input text to be said
        """
        self.replyHelper(text)
        # x = threading.Thread(target=replyHelper, args=(text,))
        # x.start()
