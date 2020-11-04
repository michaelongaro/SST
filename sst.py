from tkinter import *
from playsound import playsound
import time
from stopwatch import Stopwatch

# READ THIS: make this into a WORKING executable

class Window(Frame):


    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.master = master

        self.init_window()

        self.t_sw = Stopwatch().reset()
        self.j_sw = Stopwatch().reset()
        self.m_sw = Stopwatch().reset()
        self.a_sw = Stopwatch().reset()
        self.s_sw = Stopwatch().reset()

        self.summs_list = [self.t_sw, self.j_sw, self.m_sw, self.a_sw, self.s_sw]
        self.music_list = ['top.mp3', 'jg.mp3', 'mid.mp3', 'ad.mp3', 'supp.mp3']

    def init_window(self):

        self.master.title("Summoner Spell Timer")

        self.pack(fill=BOTH, expand=1)

        tButton = Button(self, text='Top', command=self.play_t)
        jButton = Button(self, text='Jungle', command=self.play_j)
        mButton = Button(self, text='Mid', command=self.play_m)
        aButton = Button(self, text='ADC', command=self.play_a)
        sButton = Button(self, text='Support', command=self.play_s)

        self.tRad = IntVar()
        self.tRad.set(2)
        self.jRad = IntVar()
        self.jRad.set(4)
        self.mRad = IntVar()
        self.mRad.set(6)
        self.aRad = IntVar()
        self.aRad.set(8)
        self.sRad = IntVar()
        self.sRad.set(10)

        self.radioList = [self.tRad, self.jRad, self.mRad, self.aRad, self.sRad]

        # will probably want to eventually automate this part, however this is still decent
        tRadio = Radiobutton(self, text='Has CI', variable=self.tRad, value=1)
        tRadio2 = Radiobutton(self, text="Doesn't Have CI", variable=self.tRad, value=2)

        jRadio = Radiobutton(self, text='Has CI', variable=self.jRad, value=3)
        jRadio2 = Radiobutton(self, text="Doesn't Have CI", variable=self.jRad, value=4)

        mRadio = Radiobutton(self, text='Has CI', variable=self.mRad, value=5)
        mRadio2 = Radiobutton(self, text="Doesn't Have CI", variable=self.mRad, value=6)

        aRadio = Radiobutton(self, text='Has CI',  variable=self.aRad, value=7)
        aRadio2 = Radiobutton(self, text="Doesn't Have CI", variable=self.aRad, value=8)

        sRadio = Radiobutton(self, text='Has CI', variable=self.sRad, value=9)
        sRadio2 = Radiobutton(self, text="Doesn't Have CI",  variable=self.sRad, value=10)

        tButton.place(x=10, y=40)
        jButton.place(x=10, y=90)
        mButton.place(x=10, y=140)
        aButton.place(x=10, y=190)
        sButton.place(x=10, y=240)

        tRadio.place(x=80, y=40)
        jRadio.place(x=80, y=90)
        mRadio.place(x=80, y=140)
        aRadio.place(x=80, y=190)
        sRadio.place(x=80, y=240)

        tRadio2.place(x=150, y=40)
        jRadio2.place(x=150, y=90)
        mRadio2.place(x=150, y=140)
        aRadio2.place(x=150, y=190)
        sRadio2.place(x=150, y=240)

    def client_exit(self):
        exit()

    # EVENTUALLY could want the actual seconds displayed in the application (next to the button)

    def play_t(self):
        self.t_sw.restart()

    def play_j(self):
        self.j_sw.restart()

    def play_m(self):
        self.m_sw.restart()

    def play_a(self):
        self.a_sw.restart()

    def play_s(self):
        self.s_sw.restart()


if __name__ == '__main__':

    root = Tk()
    root.geometry("300x315")

    app = Window(root)

    flash_timer_list = [0.0, 0.0, 0.0, 0.0, 0.0]


    while True:

        for index in range(len(flash_timer_list)):
            if app.radioList[index].get() % 2 == 0:
                flash_timer_list[index] = 300.0
            else:
                flash_timer_list[index] = 285.0



        # side note: if you want to be more accurate, and this looping stuff works you should sort summs_list in ascending order
        for i in range(len(app.summs_list)):
            if app.summs_list[i].duration >= flash_timer_list[i]:
                print(app.summs_list[i].duration)
                playsound(app.music_list[i])
                app.summs_list[i].reset()

        root.update_idletasks()
        root.update()
