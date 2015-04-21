from Tkinter import *
from PIL import Image, ImageTk
from subprocess import Popen, call, PIPE, STDOUT
import imp
import tkFont
import time
import os

root = Tk()

def say(words):
    google_url = "http://translate.google.com/translate_tts?tl=en&q=%s"
    subprocess.call(["mplayer", google_url % words])

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
                        relief=FLAT, background='white',
                        highlightthickness=0, font=self.font_big)
        return button


    def cb_face_r(self):
        app = Popen(["python", "./apps/face-detect/webcam_voice.py"])
        self.win = Toplevel(bg='white')
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
        self.make_fullscreen(self.win)

    	def close_app():
            app.kill()
            self.win.destroy()

        font_text = ("Helvetica", 16)

        # Use dynamic variables to set the label text
        text_var_q = StringVar()
        text_var_a = StringVar()

        text_q = Label(self.win, text=text_var_q, wraplength=600, font=font_text)
        text_a = Label(self.win, text=text_var_a, wraplength=600, font=font_text)


        def ask():
            question = qa.hear()
            text_var_q.set(question + "?\n\n")
            response = qa.answer(question)
            text_var_a.set(response)

        self.big_button(self.win, "Ask", ask).pack()
        self.big_button(self.win, "Quit", close_app).pack()

        text_q.pack()
        text_a.pack()

    def cb_pandora(self):
	    app = Popen(["pianobar"], stdin=PIPE)

        self.win = Toplevel(bg='white')
        self.make_fullscreen(self.win)

        def close():
            app.kill()
            self.win.destroy()

        var_curr_play = StringVar()

        def send_command(command):
            if command == "p":
                app.communicate(input=b"p")
                if self.b_pauseplay['text'] == "Pause":
                    self.b_pauseplay['text'] = "Play"
                else:
                    self.b_pauseplay['text'] = "Pause"
            if command == "n":
                app.communicate(input=b"n")

        font_text = ("Helvetica", 18)
        self.l_curr_play = Label(self.win, text=var_curr_play, font=font_text)

        self.l_curr_play.pack()
        self.b_pauseplay = Button(self.win, text="Pause", command=lambda: send_command("p"))
        self.b_pauseplay.pack()
        Button(self.win, text="Next", command=lambda: send_command("n")).pack()
        self.big_button(self.win, text="Quit", close).pack()


    def cb_tele(self):
        #TODO: Fix the overread error when called from python
        root.withdraw()
        #os.system("apps/apro-telechat/robot/out.sh")
        #os.system("apps/apro-telechat/robot/in_all.sh")
        Popen("wget 'http://10.0.0.14:5051/video' -O video.mjpeg &", shell=True)
        Popen("mplayer -demuxer 35 video.mjpeg", shell=True)
        #out_vid = Popen(["apps/apro-telechat/robot/out.sh"], shell=True)
        #in_vid = Popen(["apps/apro-telechat/robot/in_all.sh"], shell=True)
        # server = Popen(["python", "apps/apollo-server/server_start.py", "&"])

    def cb_obj_rec(self):
        recognizer = imp.load_source('recognizer','apps/apro-identify/recognizer.py')
        self.win = Toplevel(bg='white')
        self.make_fullscreen(self.win)

        def do_recog():
            matches = recognizer.recognize()
            say(matches[0])

        self.big_button(self.win, "Quit", command=self.win.close).pack()
        self.big_button(self.win, "Recognize", command=do_recog).pack()

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

	# Initialize
        self.createWidgets()

app = Application(master=root)
app.mainloop()
root.destroy()
