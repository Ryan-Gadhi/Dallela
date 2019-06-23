import re


def is_wake_up_word(text):
	text = re.search("(\w+)(e|i)(\w+)(a$)", text)
	if text is not None:
		return True
	return False




print(is_wake_up_word('tenida'))
