from Tkinter import *
from PIL import Image, ImageTk
from subprocess import Popen, call 
import imp
import tkFont
import time
import os

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
               font=self.font_helv, command=callback).grid(row=r, column=c, padx=5, pady=5)

    def cb_face_r(self):
	app = Popen(["python", "./apps/face-detect/webcam_voice.py"])	
	self.win = Toplevel()
    	def close_app():
	    app.kill()
	    self.win.destroy()
	Button(self.win, text="Quit", command=close_app).pack()	
	self.make_fullscreen(self.win)

    def cb_pong(self):
	#self.win = Toplevel()

    	#def close_app():
	#    app.kill()
	#    self.win.destroy()

	#Button(self.win, text="Quit", command=close_app).pack()	
	#self.make_fullscreen(self.win)
   	#root.overrideredirect(0)
	root.withdraw()
	#app = Popen(["./apps/apro-pingpong/run.sh"], shell=True)
	app = Popen(["python", "./apps/apro-pingpong/pingpong.py"])
	time.sleep(4)
   	app.kill()	
	root.deiconify()
	self.make_fullscreen(root)
	#q = imp.load_source('pingpong', 'apps/apro-pingpong/pingpong.py')	

    def cb_qa(self):
	q = imp.load_source('query', 'apps/apro-wolfram/query.py')
	qa = q.Query()
	
	self.win = Toplevel()
    	def close_app():
	    app.kill()
	    self.win.destroy()

	text_q = Label(self.win, text="")
	text_a = Label(self.win, text="")
	
	def ask():
	    question = qa.hear()
	    text_q['text'] = question
	    response = qa.answer(question)
	    text_a['text'] = response

	Button(self.win, text="Quit", command=close_app).pack()	
	Button(self.win, text="Ask", command=ask).pack()
	text_q.pack()
	text_a.pack()
	self.make_fullscreen(self.win)
    
    def cb_pandora(self):
	app = Popen(["pianobar"])

    def cb_tele(self):

	root.withdraw()
	#os.system("apps/apro-telechat/robot/out.sh")
	#os.system("apps/apro-telechat/robot/in_all.sh")
	Popen("wget 'http://10.0.0.14:5051/video' -O video.mjpeg &", shell=True)
	Popen("mplayer -demuxer 35 video.mjpeg", shell=True)
	#out_vid = Popen(["apps/apro-telechat/robot/out.sh"], shell=True)
	#in_vid = Popen(["apps/apro-telechat/robot/in_all.sh"], shell=True)
	# server = Popen(["python", "apps/apollo-server/server_start.py", "&"])

    def createWidgets(self):
	self.i_face_r = self.load_image("icons/new_face_recognition.png")
	self.i_follow = self.load_image("icons/new_follow_me.png")
	self.i_music = self.load_image("icons/new_pandora.png")
	self.i_pong = self.load_image("icons/new_pong.png")
	self.i_qa = self.load_image("icons/new_qa.jpg")
	self.i_tele = self.load_image("icons/new_telepresence.png")
	self.i_voice = self.load_image("icons/new_voice_command.png")
	self.i_obj_r = self.load_image("icons/new_obj_recognition.png")
	
	apps = [(self.i_face_r, "Facial\n Recognition", self.cb_face_r),
		(self.i_follow, "Follow Me", None),
		(self.i_music, "Music", self.cb_pandora),
		(self.i_pong, "Pong Game", self.cb_pong),
		(self.i_qa, "Q & A", self.cb_qa),
		(self.i_tele, "Teleprescence", self.cb_tele),
		(self.i_voice, "Voice\n Command", None),
		(self.i_obj_r, "Object\n Recognition", None)]
 	
	num_app = 0
	for img, name, call in apps:	
		row = num_app // 4
		col = num_app % 4
		self.create_icon(self.f, img, name, (row,col), call) 
		num_app += 1
	
    def __init__(self, master=None):
        Frame.__init__(self, master)

	# Make full screen
	w, h = 800, 480#root.winfo_screenwidth(), root.winfo_screenheight()
	root.overrideredirect(1)
	root.geometry("%dx%d+0+0" % (w, h))

	#self.i_bg = self.load_image("icons/test.png")
	#Label(root, image=self.i_bg).place(x=0,y=0, relwidth=1, relheight=1)
	root.configure(background='white')

	self.font_helv = tkFont.Font(family='Helvetica',
	    size=18, weight='bold')

	# Center the icons
        self.f = Frame(root, bg='white')
	self.f.pack(side=LEFT, expand = 1, pady = 0, padx = 0)
	
	# Initialize 
        self.createWidgets()
	
app = Application(master=root)
app.mainloop()
root.destroy()
