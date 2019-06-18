import speech_recognition as sr
import pyttsx3
import platform
from playsound import playsound


skills = []
audio_text = ''
global_engine = None

def is_in_wake_words(audio_text):
    """
    this function checks if the word
    said is one of the similar words to
    Dalela in wake_up_words.txt
    """

    file = open('wake_up_words.txt','r')

    similar_words = (file.read().split('\n'))  # making a list
    for word in similar_words:  # going over that list
        if word.lower() in audio_text.lower():
            not_wakeup_word = False
            # print('it matches ' + word)
            return True
    return False


def look_for_trigger():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        not_wakeup_word = True

        while not_wakeup_word:  # keep listening as long as no trigger word recognized
            try:
                print("I am listening :")
                input_audio = r.listen(source)
                audio_text = r.recognize_google(input_audio)
                print("You said : {}".format(audio_text))
                if is_in_wake_words(audio_text):
                    not_wakeup_word = False
            except:
                print("not recognized by the API")

    if not (not_wakeup_word):
        playsound('beep.wav')


def start_listening():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            print("I am listening :")
            input_audio = r.listen(source)
            audio_text = r.recognize_google(input_audio)
            print("You said : {}".format(audio_text))
            if is_in_wake_words(audio_text):
                not_wakeup_word = False
            return audio_text
        except:
            print("not recognized by the API")


def findOS_Sound():
    os_name = platform.system()
    name = 'undefined'
    if os_name=='Windows':
        name = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'
    elif os_name == 'Darwin':
        name = 'com.apple.speech.synthesis.voice.samantha'
    elif os_name == 'Linux':
        name = 'female3'
    else:
        print('os not recognized')
    return name

def test_audio():
    name = findOS_Sound()
    global global_engine
    global_engine = pyttsx3.init()

    try:
        global_engine.setProperty('voice', name)
        print('property has been set..')
    except():
        print('specified sound not found in the local system!')
    return global_engine




def reply(text):
    global global_engine
    engine = global_engine
    engine.say(text)
    engine.runAndWait()



