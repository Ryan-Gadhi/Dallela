import AudioUtils
import random
import os


# def __init__(self):
# 	self.chosen_question = []
# 	self.chosen_answer = []

special_files = ['shorts','Similars']
qst_dir = os.getcwd()+'/interpeter/skills/Trvial_Skill/Questions/'
ans_dir = os.getcwd()+'/interpeter/skills/Trvial_Skill/Answers/'


def search_for_match(text):
	os.chdir(qst_dir)                 # todo: questions is answers <opposite!>
	for file in os.listdir():
		line_number = readQuestionChoices(file, text)
		if line_number != -1:
			answer = readAnswerChoices(file, line_number)
			print(answer)
			AudioUtils.reply(answer)
			return True,answer
	return False,None


def readQuestionChoices(file_name, text):

	file = open(file_name)  # todo: should be changed (add .txt) when adding extentions
	questions = file.read()
	file.close()
	questions = questions.split('\n')

	line_number = 0
	for question in questions:
		if text.lower() == question.lower():
			return line_number
		line_number += 1
	return -1


def readAnswerChoices(file_name, line_number):
	os.chdir(ans_dir)

	file = open(file_name)  # todo: should be changed (add .txt) when adding extentions
	answers = file.read()
	file.close()
	answers = answers.split('\n')

	if file_name not in special_files:
		chosen_answer = random.choice(answers)
	else:
		# chosen_answer = pass
		chosen_answer = answers[line_number]

	return chosen_answer



