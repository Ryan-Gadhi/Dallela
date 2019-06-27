import platform
import re

import pyttsx3
import speech_recognition as sr
from playsound import playsound

# global_engine = None
start_listening_text = 'who are you'
wake_up_text = None
t1 = None

"""
    # currently not used
    
    checks if the audio text is in the file 
    containing words similar to Daleela
"""


def is_in_wake_wordsv1(audio_text):
    """
    this function checks if the word
    said is one of the similar words to
    Dalela in wake_up_words.txt
    """

    file = open('wake_up_words.txt', 'r')

    similar_words = (file.read().split('\n'))  # making a list
    for word in similar_words:  # going over that list
        if word.lower() in audio_text.lower():
            not_wakeup_word = False
            # print('it matches ' + word)
            return True
    return False


def get_start_listening_text():
    return start_listening_text


"""
    # this is a temporary method, should be overridden by Tenserflow
    checks if the said word feels sound like Daleela

"""


def is_in_wake_words(text):
    text = re.search("(\w+)(e|i)(\w+)(a$)", text)

    if text is not None:
        return True

    return False


#
# def look_for_trigger():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         not_wakeup_word = True
#
#         while not_wakeup_word:  # keep listening as long as no trigger word recognized
#             try:
#                 print("I am listening :")
#                 input_audio = r.listen(source)
#                 audio_text = r.recognize_google(input_audio)
#                 print("You said : {}".format(audio_text))
#                 if is_in_wake_words(audio_text):
#                     not_wakeup_word = False
#             except:
#                 print("not recognized by the API")

# if not (not_wakeup_word):
#     playsound('beep.wav')
#     return True
# return False


def start_listening(awake):
    """
        this method:
                    adds the 2 beep sounds
                    connects to google's server
                    for speech recognition

        awake: a boolean value that reflects weather
        the wake word has been said or not
    """
    global start_listening_text
    start_listening_text = None

    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            print("I am listening :")
            playsound('beep.wav')
            # global start_listening_text
            inputAudio = r.listen(source)
            print("I am sending to google")
            playsound('beep2.wav')
            start_listening_text = r.recognize_google(inputAudio)
            print("You said : {}".format(start_listening_text))

        except:
            print("not recognized by the API :\n")
            start_listening_text = 'Error_001'


"""
    this method makes a new thread to handle 
    google server connection in the background 
    
    awake: a boolean value that reflects weather
    the wake word has been said or not

"""
# def start_listening(awake):
#     global t1
#     t1 = threading.Thread(target=start_listening_Helper,args=(awake,))
#     t1.start()
#     return t1

"""
    the following is only related to pyttsx3 package
    it checks for woman sound in the local system
    and choose as the default

"""


def findOS_Sound():
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


def test_audio():
    global_engine = pyttsx3.init()
    try:
        global_engine.setProperty('voice', findOS_Sound())
        print('property has been set..')
    except:
        print('specified sound not found in the local system!')
    return global_engine

    """
        this method is responsible for the sound output
        it is called by 'reply' method to make a new thread
        text: input text to be said
           
    """


def reply(text):
    # print('audio')
    # global global_engine

    engine = test_audio()
    # print(text+ "<<<<<<<<<")
    engine.say(text)

    engine.runAndWait()
    print(text + "#from engine")

    # print('finished audio')


"""
    makes a new thread that handles the sound output 
    in a new thread
    
    text: input text to be said
"""
# def reply(text):
#     x = threading.Thread(target=replyHelper, args=(text,))
#     x.start()
