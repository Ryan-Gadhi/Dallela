from tkinter import *
from PIL import Image,ImageTk


class GUI:

	label1 = 'in in'
	label2 = 'out in'
	root = None


	def __init__(self,root,cmd1):
		self.root = root
		# frame = Frame(root)
		#
		screen_x = root.winfo_screenwidth()
		screen_y = root.winfo_screenheight()

		#
		# frame.pack()
		win_width = int(screen_x / 1.5)
		win_height = int(screen_y / 1.5)


		self.root.geometry(str(win_width) + 'x' + str(win_height))  # changes window size

		self.B = Button(root, text="Start", command=cmd1, fg='dodger blue', font='Arial 20')
		self.B.config(width=int(win_width / 120), height=int(win_height/ 240))
		self.B.place(x=win_width / 22, y=win_height / 2.05)

		self.B2 = Button(root, text="Reset", fg='dodger blue', font = 'Arial 20')
		self.B2.config(width= int(win_width / 120), height= int(win_height/ 240))
		self.B2.place(x=win_width / 22, y=win_height / 1.7)

		self.label1 = Label(root, text="This is what the user just said",font='Arial 32',fg="blue4")
		self.label1.pack()
		self.label1.place(x=win_width / 3, y=win_height / 2)


		self.label2 = Label(root, text="This is what Dallela is going to say",
		                    font='Arial 32',fg='dodger blue')
		self.label2.pack()
		self.label2.place(x=win_width / 3, y=win_height / 1.5)

		self.logo = ImageTk.PhotoImage(Image.open("bhge.png"))
		self.panel = Label(root, image=self.logo)
		self.panel.pack(side="bottom", fill="both", expand="yes")
		self.panel.place(x=screen_x - screen_x / 2, y=screen_y / 9, anchor='sw')


	def event_handler(self):
		print()


	def setUpperLabel(self,text):

		words = text.split()
		temp = ''
		limit = 8
		if len(words) > limit:
			i = 0
			for word in words:
				if (i < limit):
					temp += " " + word
				else:
					temp += '\n'
					i = 0
					temp += " " + word
				i += 1
		else:
			temp = text

		text = temp
		text = text[:1].upper()+text[1:]
		self.label1.config(text=text)

	def setBottomLabel(self,text):

		words = text.split()
		temp = ''
		limit = 8
		if len(words) > limit:
			i = 0
			for word in words:
				if (i < limit):
					temp += " " + word
				else:
					temp += '\n'
					i = 0
					temp += " " + word
				i += 1
		else:
			temp = text

		text = temp

		self.label2.config(text=text)

