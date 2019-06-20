
from AudioUtils import *
from interpeter.skills.Trvial_Skill import TrivialSkills
from tkinter import *
from PIL import Image,ImageTk


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
	# frame = Frame(root)
	#
	screen_x = root.winfo_screenwidth()
	screen_y = root.winfo_screenheight()


	#
	# frame.pack()
	win_width = int(screen_x/1.5)
	win_height = int(screen_y / 1.5)
	unit = 1

	root.geometry(str(win_width)+'x'+str(win_height))  # changes window size

	B = Button(root, text="Start",command=program_flow,fg='red',relief=RAISED)
	B.config(width=unit*12,height=unit*3)
	B.place(x=win_width/20, y=win_height/4)

	B2 = Button(root, text="Mute", fg='red', relief=RAISED)
	B2.config(width=unit * 12, height=unit * 3)
	B2.place(x=win_width / 20, y=win_height / 2.8)



	label1 = Label(root, text="This is what the user just said")
	label1.pack()
	label1.place(x=win_width/2.7, y=win_height/2)

	label2 = Label(root, text="This is what Dallela is going to say")
	label2.pack()
	label2.place(x=win_width/2.7, y=win_height/1.5)

	logo = ImageTk.PhotoImage(Image.open("bhge.png"))
	panel = Label(root, image=logo)
	panel.pack(side="bottom", fill="both", expand="yes")
	panel.place(x=screen_x-screen_x/2, y=screen_y/9, anchor='sw')

	root.mainloop()





def program_flow():
	#test_audio()
	audio_text = 'tell me a joke'
	find_skill(audio_text)



""" 
	Main code
"""


#todo: do adapt processing

if __name__ == '__main__':

	# look_for_trigger()
	# audio_text = start_listening()

	test_audio()
	drawGUI()


	# test_audio()
	# audio_text = 'tell me a joke'
	# find_skill(audio_text)


# todo: make a method that searches through skills to find the aprioperiate one (this is before nlp)

#
# input_text = 'what is the closest offset well'
# app.put_in_engin(input_text)
#

