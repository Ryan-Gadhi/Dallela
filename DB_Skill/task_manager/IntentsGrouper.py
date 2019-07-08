import os
from DB_Skill.task_manager.Intents import *
"""
this file uses exec funtion, which may create 
problems for diffente operating systems
"""
Intent_path = (os.getcwd()+'/Intents/')  # todo: should be changed according to new structure
os.chdir(Intent_path)


all_intents = []  # this
all_MRA = []  # all multi regex entities
all_entities_dic = {}
intent_files = os.listdir()

# intent_files = intent_files[1]
# intent_files = [intent_files]
# print(intent_files)

for file in intent_files:
	if file[0:2] != '__':  # throwing away non-intent files
		intent_tmp = []
		multi_regex_entities_tmp = []
		entities_tmp = []
		exec('intent_tmp = ('+file[:-3]+'.intents)')  # avoiding '.py' chars and grabing data
		exec('multi_regex_entities_tmp = (' + file[:-3] + '.multi_regex_entities)')
		exec('entities_tmp = (' + file[:-3] + '.entities)')
		for intent in intent_tmp:
			print(intent_tmp)
			all_intents.append(intent)  # extracts the intents out of the 'intents' list

		for MRA in multi_regex_entities_tmp:
			all_MRA.append(MRA)

		for name,entity in entities_tmp.items():
			all_entities_dic[name] = entity



