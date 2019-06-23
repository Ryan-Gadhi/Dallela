
from AudioUtils import *
from interpeter.skills.Trvial_Skill import TrivialSkills
from tkinter import *
from GUI import GUI
import time
from threading import Thread
from AudioUtils import reply


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

def ListenButtonAction():
	if(look_for_trigger()):
		global audio_text
		audio_text = start_listening()
		find_skill()





""" 
	Main code
"""

if __name__ == '__main__':
	audio_text = 'tell me a joke'

	# look_for_trigger()


	test_audio()
	root= Tk()
	gui = GUI.GUI(root,ListenButtonAction)
	root.mainloop()

	#audio_text = start_listening()








# todo: make a method that searches through skills to find the aprioperiate one (this is before nlp)

#
# input_text = 'what is the closest offset well'
# app.put_in_engin(input_text)
#

