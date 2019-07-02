from adapt.engine import IntentDeterminationEngine
from DB_Skill.task_manager.IntentsGrouper import all_entities_dic as entities, all_intents as intents, all_MRA as multi_regex_entities
from DB_Skill.task_manager import Handler

engine = IntentDeterminationEngine()


# Register entities in engine
for entity, keywords in entities.items():
    for keyword in keywords:
        engine.register_entity(keyword, entity)

for entity in multi_regex_entities:
    for regex in entity:
        engine.register_regex_entity(regex)

# Register intents on engine
for intent in intents:
    engine.register_intent_parser(intent)


text1= 'what is the number of active jobs today?'
text2= 'create assignment buy mic for john'


for intent in engine.determine_intent(text1):
	print (intent)

for intent in engine.determine_intent(text2):
	print (intent)


def f1():
	print(' i am connecting todo')

h1 = Handler.Handler(intents[0], f1)


h1.compute()  #
