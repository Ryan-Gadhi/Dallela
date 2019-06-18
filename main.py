from Trvial_Skill import TrivialSkills
from AudioUtils import *
from Trvial_Skill import TrivialSkills
from DB_Skill.task_manager1 import app

def find_skill(text):
	"""
	checks if the skill is DB or Trivial or DuckDuckGo
	"""
	skill_found = TrivialSkills.search_for_match(text)  # this will say if match found

	if (not skill_found):
		pass
	# search for the Question in the DB
	#
	#

""" 
	Main code
"""

#todo: do adapt processing

# look_for_trigger()
# audio_text = start_listening()
test_audio()
audio_text = 'tell me a joke'
find_skill(audio_text)


# todo: make a method that searches through skills to find the aprioperiate one (this is before nlp)

#
# input_text = 'what is the closest offset well'
# app.put_in_engin(input_text)
#

