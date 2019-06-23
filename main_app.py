
from AudioUtils import *
from interpeter.skills.Trvial_Skill import TrivialSkills
from tkinter import *
from GUI import GUI
import time
from threading import Thread
from AudioUtils import *


def find_skill():
	"""
	checks if the skill is DB or Trivial or DuckDuckGo
	"""
	answer = 'Error'


	skill_found,answer = TrivialSkills.search_for_match(audio_text)  # this will say if match found
	if (not skill_found):
		pass

	global gui
	gui.setBottomLabel(answer)
	gui.setUpperLabel(audio_text)
	print('gui updated')

	reply(answer)
	# search for the Question in the DB
	#

def LookForSkill():
	# if(look_for_trigger()):
	#t2 = threading.Thread(target=checkerThread)
	global audio_text
	audio_text = get_start_listening_text()
	find_skill()

def ButtonClicked():
	# trigger
	t1 = start_listening()
	t2 = threading.Thread(target= waitForResponse, args=(t1,))
	t2.start()


def waitForResponse(t1):
	while (t1.is_alive()):
		pass
	print(get_start_listening_text() + ' <-00->')
	LookForSkill()  # when google responds we search for the skill


""" 
	Main code
"""

if __name__ == '__main__':
	audio_text = 'tell me a joke'

	# look_for_trigger()


	test_audio()
	root= Tk()
	gui = GUI.GUI(root,ButtonClicked)
	root.mainloop()

	#audio_text = start_listening()








# todo: make a method that searches through skills to find the aprioperiate one (this is before nlp)

#
# input_text = 'what is the closest offset well'
# app.put_in_engin(input_text)
#

