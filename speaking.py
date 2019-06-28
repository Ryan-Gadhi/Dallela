import platform
import threading
import pyttsx3



class Speak:

	def __init__(self):
		self.engine = pyttsx3.init()

	def say(self,text):
		if text=='':
			return
		self.engine.say(text)
		print('run and wait')
		self.engine.runAndWait()

	def findOS_Sound(self):
		os_name = platform.system()
		name = 'undefined'
		if os_name == 'Windows':
			name = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'
		elif os_name == 'Darwin':
			name = 'com.apple.speech.synthesis.voice.samantha'
		elif os_name == 'Linux':
			name = 'female3'
		else:
			print('os not recognized')
		return name


	def womanAudio(self):
		name = self.findOS_Sound()
		print(self)
		try:
			self.engine.setProperty('voice', name)
			print('women voice has been set')
		except():
			print('specified sound not found in the local system!')


def startThread():
	sp = Speak()
	sp.womanAudio()
	sp.say('i am a teenager')


spThread = threading.Thread(target=startThread)
spThread.start()




# creating multiple instance uses the same sound configuration
# passing '' to say freezes the application (handled)

