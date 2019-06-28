import speech_recognition as sr
from playsound import playsound



def start_listening_Helper():
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

start_listening_Helper()