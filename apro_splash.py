#!/usr/bin/python
from Tkinter import *
from PIL import Image, ImageTk
from subprocess import Popen, call, PIPE, STDOUT, check_call
import imp
import tkFont
import time
import os

root = Tk()

def say(words):
    google_url = "http://translate.google.com/translate_tts?tl=en&q=%s"
    call(["mplayer", google_url % words])

class Application(Frame):
    def load_image(self, image):
        icon_pil = Image.open(image)
        return  ImageTk.PhotoImage(icon_pil)

    def make_fullscreen(self, window):
        w, h = window.winfo_screenwidth(), window.winfo_screenheight()
        window.overrideredirect(1)
        window.geometry("%dx%d+0+0" % (w, h))
        window.lift()

    def create_icon(self, parent, img, name, position, callback):
        r, c = position
        Button(parent, compound=TOP, image=img, relief=FLAT,
            background='white', highlightthickness=0, text=name,
               font=self.font_helv, command=callback).grid(row=r, column=c, padx=5, pady=5)

    def big_button(self, window, string, function):
        font_big = tkFont.Font(family='Helvetica',
                               size=24, weight='bold')
        button = Button(window, text=string, command=function,
                        relief=FLAT, bg='white',
                        highlightthickness=0, padx=15, pady=15,font=font_big)
        return button

    def set_background(self, window):
	myvar=Label(window,image=self.i_bg)
	myvar.place(x=0, y=0, relwidth=1, relheight=1)

    def cb_face_r(self):
        app = Popen(["python", "./apps/face-detect/webcam_voice.py"])
        self.win = Toplevel(bg='white')

	self.set_background(self.win)
        self.make_fullscreen(self.win)

    	def close_app():
            app.kill()
            self.win.destroy()

        self.big_button(self.win, "Quit", close_app).pack()

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
        time.sleep(30)
        app.kill()
        root.deiconify()
        self.make_fullscreen(root)
	#q = imp.load_source('pingpong', 'apps/apro-pingpong/pingpong.py')

    def cb_qa(self):
        q = imp.load_source('query', 'apps/apro-wolfram/query.py')
        qa = q.Query()

        self.win = Toplevel(bg='white')

	self.set_background(self.win)
        self.make_fullscreen(self.win)

    	def close_app():
            self.win.destroy()

        font_text = ("Helvetica", 20)

        # Use dynamic variables to set the label text
        text_var_q = StringVar()
        text_var_a = StringVar()

        text_q = Label(self.win,bg='white', textvariable=text_var_q, wraplength=600, font=font_text)
        text_a = Label(self.win,bg='white', textvariable=text_var_a, wraplength=600, font=font_text)


        def ask():
            question = qa.hear()
            text_var_q.set(question + "?\n")
            response = qa.answer(question)
            text_var_a.set(response)

	fr = Frame(self.win, width=125, height=100, bg='white')
	fr.pack(side=BOTTOM)
        self.big_button(fr, "Ask", ask).pack(pady=25, side=LEFT)
        self.big_button(fr, "Quit", close_app).pack(side=LEFT)

        text_q.pack()
        text_a.pack()

    def cb_pandora(self):
    	app = Popen(["pianobar"], stdin=PIPE, stdout=PIPE)

        self.win = Toplevel(bg='white')
        self.make_fullscreen(self.win)

        def close():
            app.kill()
            self.win.destroy()

        var_curr_play = StringVar()
	
        def send_command(command):
            app.stdin.write(command)

            if command == "p":
                if self.b_pauseplay['text'] == "Pause":
                    self.b_pauseplay['text'] = "Play"
                else:
                    self.b_pauseplay['text'] = "Pause"

        font_text = ("Helvetica", 18)
        self.l_curr_play = Label(self.win,bg='white', textvariable=var_curr_play, font=font_text)

        self.l_curr_play.pack()
        self.b_pauseplay = self.big_button(self.win, "Pause", lambda: send_command("p"))
        self.b_pauseplay.pack()
        self.big_button(self.win, "Next", lambda: send_command("n")).pack()
        self.big_button(self.win, "V+", lambda:send_command(")")).pack()
        self.big_button(self.win, "V-", lambda:send_command("(")).pack()
        self.big_button(self.win, "Quit", close).pack()


    def cb_tele(self):
        #TODO: Fix the overread error when called from python
        root.withdraw()
        #os.system("apps/apro-telechat/robot/out.sh")
        #os.system("apps/apro-telechat/robot/in_all.sh")
        #Popen("wget 'http://10.0.0.14:5051/video' -O video.mjpeg &", shell=True)
        #Popen("mplayer -demuxer 35 video.mjpeg", shell=True)
        call(["./apps/apro-telechat/robot/out.sh"], shell=True)
        os.spawnl(os.P_NOWAIT, "./apps/apro-telechat/robot/in_all.sh")
        # server = Popen(["python", "apps/apollo-server/server_start.py", "&"])

    def cb_obj_rec(self):
        recognizer = imp.load_source('recognizer','apps/apro-identify/recognizer.py')
        self.win = Toplevel(bg='white')
	self.set_background(self.win)
        self.make_fullscreen(self.win)
        var_items = StringVar()
        def do_recog():

	    root.withdraw()
            matches = recognizer.recognize()
	    
	    call("convert picture.jpeg -resize 800x480! picture.jpeg", shell=True)
	    self.win.withdraw()
	    img = Popen(["display","+borderwidth","-backdrop","picture.jpeg"])
            say("I see a " + matches[0] + " or more specifically a " + matches[5])
	    img.kill()
	    root.deiconify()
	    self.win.deiconify()
	    self.make_fullscreen(root)
	    self.make_fullscreen(self.win)
            str_form = ""
            num = 1
            for item in matches:
                str_form += item + ",   "
                if num % 2 == 0:
                    str_form += "\n"
                num += 1
	    var_items.set(str_form)

	self.big_button(self.win, "Quit", self.win.destroy).pack()
        self.big_button(self.win, "Recognize", do_recog).pack()
        Label(self.win, pady=50, font=("Helvetica", 18),textvariable=var_items, bg='white').pack(fill=X)

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
            (self.i_obj_r, "Object\n Recognition", self.cb_obj_rec)]

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
	
	self.i_bg = self.load_image("background.png")

	# Initialize
        self.createWidgets()

app = Application(master=root)
app.mainloop()
root.destroy()
