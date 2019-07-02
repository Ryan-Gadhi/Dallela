
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
<<<<<<< HEAD
au = AudioUtils()
||||||| merged common ancestors
=======
au = AudioUtils()


def find_skill(text):
    """
    checks if the skill is DB or Trivial or DuckDuckGo
>>>>>>> 8a9b78e950abf9841e5ef7fc3533fffa4398f5ca

<<<<<<< HEAD
||||||| merged common ancestors
def find_skill():
	"""
	checks if the skill is DB or Trivial or DuckDuckGo

	"""
=======
    """
    if text is None or text == '':
        return None

    found,answer = TrivialSkills.search_for_match(text)  # this will say if match found
    if found:
        return answer
>>>>>>> 8a9b78e950abf9841e5ef7fc3533fffa4398f5ca

<<<<<<< HEAD
def find_skill(text):
    """
    checks if the skill is DB or Trivial or DuckDuckGo
||||||| merged common ancestors
	print(audio_text)
	skill_found,answer = TrivialSkills.search_for_match(audio_text)  # this will say if match found
=======
    if not found:
        print(' ### Request not found in trivial skills')
>>>>>>> 8a9b78e950abf9841e5ef7fc3533fffa4398f5ca

<<<<<<< HEAD
    """
    if text is None or text == '':
        return None
||||||| merged common ancestors
	if (not skill_found):
		print('Skill not found in Trivial skills --- XXX')
=======
        original_dir = os.getcwd()
        os.chdir(os.getcwd()+'/interpeter/')
>>>>>>> 8a9b78e950abf9841e5ef7fc3533fffa4398f5ca

<<<<<<< HEAD
    found,answer = TrivialSkills.search_for_match(text)  # this will say if match found
    if found:
        return answer
||||||| merged common ancestors
		original_dir = os.getcwd()
		os.chdir(os.getcwd()+'/interpeter/')
		engine = Engine()
		os.chdir(original_dir)
		answer = engine.compute(audio_text)
		answer+= '. Sorry for taking so long to answer. The network is slow in this building'
		if(answer is None):  # not found in the database
			pass
=======
        engine = Engine()
        os.chdir(original_dir)
>>>>>>> 8a9b78e950abf9841e5ef7fc3533fffa4398f5ca

<<<<<<< HEAD
    if not found:
        print(' ### Request not found in trivial skills')
||||||| merged common ancestors
=======
        answer = engine.compute(text)
>>>>>>> 8a9b78e950abf9841e5ef7fc3533fffa4398f5ca

<<<<<<< HEAD
        original_dir = os.getcwd()
        os.chdir(os.getcwd()+'/interpeter/')
||||||| merged common ancestors
	# or connect to Duck Duck go api
=======
        if answer is not None and answer != '':  # not found in the database
            return answer   
      
        else:
            text = 'Error_101'  # question not found: either not recognized correctly or not actually implemented
            found, answer = TrivialSkills.search_for_match(text)
            return 'Error_101'
>>>>>>> 8a9b78e950abf9841e5ef7fc3533fffa4398f5ca

<<<<<<< HEAD
        engine = Engine()
        os.chdir(original_dir)
||||||| merged common ancestors
	global gui
	gui.setBottomLabel(answer)
	gui.setUpperLabel(audio_text)
	print('gui updated')
=======
    # or connect to Duck Duck go api

    # global gui
    # gui.setBottomLabel(answer)
    # gui.setUpperLabel(audio_text)
    # print('gui updated')
>>>>>>> 8a9b78e950abf9841e5ef7fc3533fffa4398f5ca

<<<<<<< HEAD
        answer = engine.compute(text)
||||||| merged common ancestors
	reply(answer)  # say the answer out loud
	#
=======
>>>>>>> 8a9b78e950abf9841e5ef7fc3533fffa4398f5ca

        if answer is not None and answer != '':  # not found in the database
            return answer   
      
        else:
            text = 'Error_101'  # question not found: either not recognized correctly or not actually implemented
            found, answer = TrivialSkills.search_for_match(text)
            return 'Error_101'

<<<<<<< HEAD
    # or connect to Duck Duck go api
||||||| merged common ancestors
def LookForSkill():
	"""
	fetches the audio text
	then calls find skill
=======
def LookForSkill():
    """
    fetches the audio text
    then calls find skill
>>>>>>> 8a9b78e950abf9841e5ef7fc3533fffa4398f5ca

<<<<<<< HEAD
    # global gui
    # gui.setBottomLabel(answer)
    # gui.setUpperLabel(audio_text)
    # print('gui updated')
||||||| merged common ancestors
	"""
	# if(look_for_trigger()):
	#t2 = threading.Thread(target=checkerThread)
	global audio_text
	audio_text = get_start_listening_text()
=======
    """
    # if(look_for_trigger()):
    #t2 = threading.Thread(target=checkerThread)
    global audio_text
    audio_text = au.get_start_listening_text()
>>>>>>> 8a9b78e950abf9841e5ef7fc3533fffa4398f5ca

<<<<<<< HEAD
||||||| merged common ancestors
	if(audio_text is None):
		audio_text = 'Error_001'
	find_skill()
=======
    if(audio_text is None):
        audio_text = 'Error_001'
    find_skill()
>>>>>>> 8a9b78e950abf9841e5ef7fc3533fffa4398f5ca


<<<<<<< HEAD
def LookForSkill():
    """
    fetches the audio text
    then calls find skill
||||||| merged common ancestors
def LookForTrigger():
	"""
		this method is called after the start button
		is clicked in the GUI. it creates 2 threads
=======
def LookForTrigger():
    """
        this method is called after the start button
        is clicked in the GUI. it creates 2 threads
>>>>>>> 8a9b78e950abf9841e5ef7fc3533fffa4398f5ca

<<<<<<< HEAD
    """
    # if(look_for_trigger()):
    #t2 = threading.Thread(target=checkerThread)
    global audio_text
    audio_text = au.get_start_listening_text()
||||||| merged common ancestors
			t1: to handle the listening/server connection
				in the background
=======
            t1: to handle the listening/server connection
                in the background
>>>>>>> 8a9b78e950abf9841e5ef7fc3533fffa4398f5ca

<<<<<<< HEAD
    if(audio_text is None):
        audio_text = 'Error_001'
    find_skill()
||||||| merged common ancestors
			t2: checks if t1 has finished and complete the
				program flow
	"""
	t1 = start_listening(awake)
	t2 = threading.Thread(target= waitForResponse, args=(t1,))
	t2.start()
=======
            t2: checks if t1 has finished and complete the
                program flow
    """
    t1 = au.start_listening(awake)
    t2 = threading.Thread(target= waitForResponse, args=(t1,))
    t2.start()
>>>>>>> 8a9b78e950abf9841e5ef7fc3533fffa4398f5ca


<<<<<<< HEAD
def LookForTrigger():
    """
        this method is called after the start button
        is clicked in the GUI. it creates 2 threads
||||||| merged common ancestors
def waitForResponse(t1):
	"""
		checks if the thread handling the google speech recognition
		has finished execution. It implements the wake word functionality
		and starts to listen for skill search
=======
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
>>>>>>> 8a9b78e950abf9841e5ef7fc3533fffa4398f5ca

<<<<<<< HEAD
            t1: to handle the listening/server connection
                in the background
||||||| merged common ancestors
		t1: gets the thread t1 to check for its life
	"""
=======
>>>>>>> 8a9b78e950abf9841e5ef7fc3533fffa4398f5ca

<<<<<<< HEAD
            t2: checks if t1 has finished and complete the
                program flow
    """
    t1 = au.start_listening(awake)
    t2 = threading.Thread(target= waitForResponse, args=(t1,))
    t2.start()
||||||| merged common ancestors
	global awake
	while (t1.is_alive()):
		pass
=======
if __name__ == '__main__':
    """
        MAIN CODE
    """
>>>>>>> 8a9b78e950abf9841e5ef7fc3533fffa4398f5ca

<<<<<<< HEAD
||||||| merged common ancestors
	heared_word = get_start_listening_text()
=======
    # audio_text = 'What is the nearest field within 5 km ?'
>>>>>>> 8a9b78e950abf9841e5ef7fc3533fffa4398f5ca

<<<<<<< HEAD
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
||||||| merged common ancestors
	if(awake):
		LookForSkill()  # when google responds we search for the skill
	elif(not awake):
		if is_in_wake_words(heared_word):
			awake = True
			LookForTrigger()
		else:
			LookForTrigger()
=======
    sp = Speaking()
    sp.womanAudio()
>>>>>>> 8a9b78e950abf9841e5ef7fc3533fffa4398f5ca


<<<<<<< HEAD
if __name__ == '__main__':
    """
        MAIN CODE
    """

    # audio_text = 'What is the nearest field within 5 km ?'

    sp = Speaking()
    sp.womanAudio()



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



    # root= Tk()
    # gui = GUI.GUI(root,LookForTrigger)
    # root.mainloop()
    # not needed #find_skill()
||||||| merged common ancestors
if __name__ == '__main__':



	#audio_text = 'What is the nearest field within 5 km ?'



	test_audio() # change to woman audio
	root= Tk()
	gui = GUI.GUI(root,LookForTrigger)
	root.mainloop()
	#not needed #find_skill()

	#not needed #audio_text = start_listening()
=======
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
>>>>>>> 8a9b78e950abf9841e5ef7fc3533fffa4398f5ca




