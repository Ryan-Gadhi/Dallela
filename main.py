from AudioUtils import *
from interpeter.skills.Trvial_Skill import TrivialSkills
from tkinter import *
from GUI import GUI


def find_skill():
    """
	checks if the skill is DB or Trivial or DuckDuckGo
	"""
    answer = 'Error'
    # audio_text = 'tell me a joke'
    skill_found, answer = TrivialSkills.search_for_match(audio_text)  # this will say if match found
    if not skill_found:
        pass

    gui
    gui.setlabel(audio_text, answer)


# search for the Question in the DB
#


""" 
	Main code
"""

if __name__ == '__main__':
    audio_text = 'tell me a joke'

    # look_for_trigger()
    # audio_text = start_listening()

    test_audio()

    root = Tk()
    gui = GUI.GUI(root, find_skill)
    root.mainloop()

# test_audio()
# audio_text = 'tell me a joke'
# find_skill(audio_text)

# todo: make a method that searches through skills to find the aprioperiate one (this is before nlp)

#
# input_text = 'what is the closest offset well'
# app.put_in_engin(input_text)
#
