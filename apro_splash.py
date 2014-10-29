from Tkinter import *
from PIL import Image, ImageTk

root = Tk()

class Application(Frame):
    def say_hi(self):
        print("hi there, everyone!")
    
    def load_image(self, image):
        icon_pil = Image.open(image)
        return  ImageTk.PhotoImage(icon_pil)

    def make_fullscreen(self, window):
	w, h = window.winfo_screenwidth(), window.winfo_screenheight()
	window.overrideredirect(1)
	window.geometry("%dx%d+0+0" % (w, h))
	window.lift()

    def create_window(self):
	self.win = Toplevel()
        self.label = Label(self.win, text="Let's see if this works")
	self.but = Button(self.win, text="Cancel", command=self.win.destroy)
        self.label.pack()
	self.but.pack() 
	self.make_fullscreen(self.win)
    
    def create_icon(self, parent, img, name, position, callback):
	r, c = position
	Button(parent, compound=TOP, image=img, relief=FLAT, 
	       background='white', highlightthickness=0, text=name, 
	       command=callback).grid(row=r, column=c, padx=25, pady=25)

    def cb_face_r(self):
	pass		

    def createWidgets(self):
	self.i_face_r = self.load_image("icons/new_face_recognition.png")
	self.i_follow = self.load_image("icons/new_follow_me.png")
	self.i_music = self.load_image("icons/new_pandora.png")
	self.i_pong = self.load_image("icons/new_pong.png")
	self.i_qa = self.load_image("icons/new_qa.jpg")
	self.i_tele = self.load_image("icons/new_telepresence.png")
	self.i_voice = self.load_image("icons/new_voice_command.png")
	self.i_obj_r = self.load_image("icons/new_obj_recognition.png")
	
	apps = [(self.i_face_r, "Facial Recognition", None),
		(self.i_follow, "Follow Me", None),
		(self.i_music, "Music", None),
		(self.i_pong, "Pong Game", None),
		(self.i_qa, "Q & A", None),
		(self.i_tele, "Teleprescence", None),
		(self.i_voice, "Voice Command", None),
		(self.i_obj_r, "Object Recognition", None)]
 	
	num_app = 0
	for img, name, call in apps:	
		row = num_app // 4
		col = num_app % 4
		self.create_icon(self.f, img, name, (row,col), call) 
		num_app += 1
	
    def __init__(self, master=None):
        Frame.__init__(self, master)

	# Make full screen
	w, h = root.winfo_screenwidth(), root.winfo_screenheight()
	root.overrideredirect(1)
	root.geometry("%dx%d+0+0" % (w, h))

	#self.i_bg = self.load_image("icons/test.png")
	#Label(root, image=self.i_bg).place(x=0,y=0, relwidth=1, relheight=1)
	root.configure(background='white')


        self.f = Frame(root, bg='white')
	self.f.pack(side=LEFT, expand = 1, pady = 50, padx = 50)
	
        self.createWidgets()
app = Application(master=root)
app.mainloop()
root.destroy()
