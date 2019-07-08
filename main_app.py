
from AudioUtils import *
from interpeter.skills.Trvial_Skill import TrivialSkills
from tkinter import *
from GUI import GUI
import time
from threading import Thread
from AudioUtils import AudioUtils
from interpeter.engine import Engine
import os
from speaking import Speaking
from triggerWord import TriggerWord

awake = False
au = AudioUtils()


def find_skill(text):
    """
    checks if the skill is DB or Trivial or DuckDuckGo

    """
    if text is None or text == '':
        return None

    found,answer = TrivialSkills.search_for_match(text)  # this will say if match found
    if found:
        return answer

    if not found:
        print(' ### Request not found in trivial skills')

        original_dir = os.getcwd()
        os.chdir(os.getcwd()+'/interpeter/')

        engine = Engine()
        os.chdir(original_dir)

        answer = engine.compute(text)

        if answer is not None and answer != '':  # not found in the database
            return answer   
      
        else:
            text = 'Error_101'  # question not found: either not recognized correctly or not actually implemented
            found, answer = TrivialSkills.search_for_match(text)
            return 'Error_101'

    # or connect to Duck Duck go api

    # global gui
    # gui.setBottomLabel(answer)
    # gui.setUpperLabel(audio_text)
    # print('gui updated')



def LookForSkill():
    """
    fetches the audio text
    then calls find skill

    """
    # if(look_for_trigger()):
    #t2 = threading.Thread(target=checkerThread)
    global audio_text
    audio_text = au.get_start_listening_text()

    if(audio_text is None):
        audio_text = 'Error_001'
    find_skill()


def LookForTrigger():
    """
        this method is called after the start button
        is clicked in the GUI. it creates 2 threads

            t1: to handle the listening/server connection
                in the background

            t2: checks if t1 has finished and complete the
                program flow
    """
    t1 = au.start_listening(awake)
    t2 = threading.Thread(target= waitForResponse, args=(t1,))
    t2.start()


def waitForResponse(t1):
    """
        checks if the thread handling the google speech recognition
        has finished execution. It implements the wake word functionality
        and starts to listen for skill search

        t1: gets the thread t1 to check for its life
    """

    global awake
    while (t1.is_alive()):
        pass

    heared_word = au.get_start_listening_text()

    if(awake):
        LookForSkill()  # when google responds we search for the skill
    elif(not awake):
        if au.is_in_wake_words(heared_word):
            awake = True
            LookForTrigger()
        else:
            LookForTrigger()


def listen():
    thread_1 = None
    while True:
        if tr.is_awake():
            time.sleep(2)
            thread_1 = au.start_listening()
            break
    while thread_1.is_alive():
        pass
    else:
        text = au.listening_text
        return text


if __name__ == '__main__':
    """
        MAIN CODE
    """

    # audio_text = 'What is the nearest field within 5 km ?'

    sp = Speaking()
    sp.womanAudio()


    # root= Tk()
    # gui = GUI.GUI(root,LookForTrigger)
    # root.mainloop()


    while True: # always listening
        print('outer')
        tr = TriggerWord()
        tr.recognize()

        while not tr.is_awake():
            pass
            # time.sleep(2)
            # print(' ***')
            # tr.threads_life()
            # print(' ### ')

        counter = 0
        limit = 2
        if tr.is_awake() == True:
            while True:  # do while style
                print('inner')
                if counter >= limit:
                    output_text = find_skill('Sleep_101')
                    sp.say(output_text)
                    break

                input_text = listen()

                if input_text == 'Error_101':
                    counter += 1
                    error_text = find_skill(input_text)
                    sp.say(error_text)

                else:
                    answer = find_skill(input_text)
                    print('entered')
                    if answer == 'Error_101':
                        counter += 1
                        output_text = find_skill(answer)
                        sp.say(output_text)
                    else:
                        sp.say(answer)
                        break



    # not needed #find_skill()
    #v0.1




