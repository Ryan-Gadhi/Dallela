
from AudioUtils import *
from interpeter.skills.Trvial_Skill import TrivialSkills
from tkinter import *
from GUI import GUI
import time
from threading import Thread
from AudioUtils import *
from interpeter.engine import Engine
import os

awake = False

def find_skill():
	"""
	checks if the skill is DB or Trivial or DuckDuckGo

	"""

	print(audio_text)
	skill_found,answer = TrivialSkills.search_for_match(audio_text)  # this will say if match found

	if (not skill_found):
		print('Skill not found in Trivial skills --- XXX')

		original_dir = os.getcwd()
		os.chdir(os.getcwd()+'/interpeter/')
		engine = Engine()
		os.chdir(original_dir)
		answer = engine.compute(audio_text)

		if(answer is None): # not found in the database
			pass


	# or connect to Duck Duck go api

	global gui
	gui.setBottomLabel(answer)
	gui.setUpperLabel(audio_text)
	print('gui updated')

	reply(answer)  # say the answer out loud
	#


def LookForSkill():
	"""
	fetches the audio text
	then calls find skill

	"""
	# if(look_for_trigger()):
	#t2 = threading.Thread(target=checkerThread)
	global audio_text
	audio_text = get_start_listening_text()

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
	t1 = start_listening(awake)
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

	heared_word = get_start_listening_text()

	if(awake):
		LookForSkill()  # when google responds we search for the skill
	elif(not awake):
		if is_in_wake_words(heared_word):
			awake = True
			LookForTrigger()
		else:
			LookForTrigger()

""" 
	Main code
"""

if __name__ == '__main__':



	#audio_text = 'What is the nearest field within 5 km ?'



	test_audio() # change to woman audio
	root= Tk()
	gui = GUI.GUI(root,LookForTrigger)
	root.mainloop()
	#not needed #find_skill()

	#not needed #audio_text = start_listening()




