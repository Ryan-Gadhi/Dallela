class Handler:
	def __init__(self,intent,func):
		self.intent = intent
		self.func = func

	def compute(self):
		self.func()




