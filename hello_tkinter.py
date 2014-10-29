from Tkinter import *
from PIL import Image, ImageTk

root = Tk()

class Application(Frame):
    def say_hi(self):
        print("hi there, everyone!")

    def createWidgets(self):
        test_icon_pil = Image.open("test.png")
        self.test_icon = ImageTk.PhotoImage(test_icon_pil)
	
	self.im = Button(compound=TOP, image=self.test_icon, relief=FLAT, background='white', highlightthickness=0, text="Demo")
	self.im.grid(row=1, column=1)
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid(padx=50, pady=50)
        self.createWidgets()
	w, h = root.winfo_screenwidth(), root.winfo_screenheight()
	root.overrideredirect(1)
	root.geometry("%dx%d+0+0" % (w, h))
	root.configure(background='white')

app = Application(master=root)
app.mainloop()
root.destroy()
