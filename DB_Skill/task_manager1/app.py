from adapt.engine import IntentDeterminationEngine
from DB_Skill.task_manager1.adapt_intents import *


def put_in_engin(text):
	engine = IntentDeterminationEngine()

	# Register entities on engine
	for entity, keywords in entities.items():
		for keyword in keywords:
			engine.register_entity(keyword, entity)

	for entity in multi_regex_entities:
		for regex in entity:
			engine.register_regex_entity(regex)

	# Register intents on engine
	for intent in intents:
		engine.register_intent_parser(intent)

	for intent in engine.determine_intent(text):
		# return dict[intenct] # will return function
		print(intent)

	print('finished')


# testing

# text1= 'what is the closest offset well hello world!'
# text2= 'where is the furthest aramco office'
# text2= 'furthest aramco office where is the '
#
#
