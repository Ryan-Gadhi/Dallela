from tkinter import *
from main_app import *

def drawGUI():
	root = Tk()
	frame = Frame(root)

	screen_x = root.winfo_screenwidth()
	screen_y = root.winfo_screenheight()

	frame.pack()
	root.geometry(str(int(screen_x/1.5))+'x'+str(int(screen_y/1.5)))  # changes window size


	b1 = Button(frame, text='Red', fg='red', command=program_flow)
	b1.pack()

	label1 = Label(frame, text="This is what the user just said")
	label1.pack()

	label2 = Label(frame, text="This is what Dallela is going to say")
	label2.pack()

	load = Image.open('bhge.png')
	render = ImageTk.PhotoImage(load)

	root.mainloop()

