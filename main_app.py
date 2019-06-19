from tkinter import *
from AudioUtils import *
from interpeter.skills.Trvial_Skill import TrivialSkills



def find_skill(text):
	"""
	checks if the skill is DB or Trivial or DuckDuckGo
	"""
	skill_found = TrivialSkills.search_for_match(text)  # this will say if match found
	print('finished search for trivial')
	if (not skill_found):
		pass
	# search for the Question in the DB
	#
	#


def drawGUI():
	root = Tk()
	frame = Frame(root)
	frame.pack()
	root.geometry("100x100")

	frame1 = Frame(root)

	b1 = Button(frame, text='Red', fg='red',command=program_flow)
	b1.pack()
	root.mainloop()


def program_flow():
	test_audio()
	audio_text = 'tell me a joke'
	find_skill(audio_text)


""" 
	Main code
"""


#todo: do adapt processing

# look_for_trigger()
# audio_text = start_listening()

drawGUI()



# test_audio()
# audio_text = 'tell me a joke'
# find_skill(audio_text)


# todo: make a method that searches through skills to find the aprioperiate one (this is before nlp)

#
# input_text = 'what is the closest offset well'
# app.put_in_engin(input_text)
#

