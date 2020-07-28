from tkinter import *
from playsound import playsound
from stopwatch import Stopwatch
import pynput.keyboard as kb
import pynput.mouse as ms
from PIL import ImageTk, Image
import time

# make button's darkgray value stay even if button is pressed
# look at event params and if they need to be used + "unused" vars in add_new_summ()


def summ_rounder(t_var, other):
    if 53 <= other % 60 <= 59:
        t_var = '59'
    elif 0 <= other % 60 < 8:
        t_var = ''
    elif 8 <= other % 60 < 23:
        t_var = '15'
    elif 23 <= other % 60 < 38:
        t_var = '30'
    elif 38 <= other % 60 < 53:
        t_var = '45'
    return t_var


class Window(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)

        self.master = master

        self.master.title("SST")

        self.pack()

        # initializing mouse + keyboard objects to be used in prnt_scrpt() and del_sums_scrpt()
        self.keyboard = kb.Controller()
        self.mouse = ms.Controller()

        # Game Timer
        self.game_sw = Stopwatch()

        # Individual Role Timer Objects
        self.t_sw = self.j_sw = self.m_sw = self.a_sw = self.s_sw = Stopwatch().reset()

        # vars to store ss cds for CheckButtons
        self.top_ci = self.jg_ci = self.mid_ci = self.ad_ci = self.supp_ci = IntVar(master)

        self.summs_list = [self.t_sw, self.j_sw, self.m_sw, self.a_sw, self.s_sw]
        self.ci_list = [self.top_ci, self.jg_ci, self.mid_ci, self.ad_ci, self.supp_ci]
        self.delay_list = [0, 0, 0, 0, 0]
        self.music_list = ['extras/top.mp3', 'extras/jg.mp3', 'extras/mid.mp3', 'extras/ad.mp3', 'extras/supp.mp3']

        top_img = ImageTk.PhotoImage(Image.open("extras/top.png"))
        jg_img = ImageTk.PhotoImage(Image.open("extras/jg.png"))
        mid_img = ImageTk.PhotoImage(Image.open("extras/mid.png"))
        ad_img = ImageTk.PhotoImage(Image.open("extras/ad.png"))
        supp_img = ImageTk.PhotoImage(Image.open("extras/supp.png"))

        # Individual Role Buttons + images + placing them on grid
        self.tButton = Button(self, height=50, width=75, image=top_img, command=self.swtch_top)
        self.tButton.image = top_img
        self.tButton.grid(row=0, column=1, columnspan=3, sticky=W+E, padx=5, pady=(5, 1))

        self.jButton = Button(self, width=10, height=50, image=jg_img, command=self.swtch_jg)
        self.jButton.image = jg_img
        self.jButton.grid(row=1, column=1, columnspan=3, sticky=W+E, padx=5, pady=1)

        self.mButton = Button(self, width=10, height=50, image=mid_img, command=self.swtch_mid)
        self.mButton.image = mid_img
        self.mButton.grid(row=2, column=1, columnspan=3, sticky=W+E, padx=5, pady=1)

        self.aButton = Button(self, width=10, height=50, image=ad_img, command=self.swtch_ad)
        self.aButton.image = ad_img
        self.aButton.grid(row=3, column=1, columnspan=3, sticky=W+E, padx=5, pady=1)

        self.sButton = Button(self, width=10, height=50, image=supp_img, command=self.swtch_supp)
        self.sButton.image = supp_img
        self.sButton.grid(row=4, column=1, columnspan=3, sticky=W+E, padx=5)

        # Delay Buttons + placing them on grid
        self.add15Button = Button(self, width=8, height=3, text="+15", command=self.swtch15)
        self.add15Button.grid(row=0, column=6, columnspan=2, sticky=E, pady=(5, 1))
        self.add30Button = Button(self, width=8, height=3, text="+30", command=self.swtch30)
        self.add30Button.grid(row=2, column=6, columnspan=2, sticky=E, pady=1)
        self.add45Button = Button(self, width=8, height=3, text="+45", command=self.swtch45)
        self.add45Button.grid(row=4, column=6, columnspan=2, sticky=E, pady=1)

        # Cosmic Insight Checkbuttons (for each role) + placing them on grid
        self.t_ci = Checkbutton(self, variable=self.top_ci, onvalue=285, offvalue=300)
        self.t_ci.grid(row=0, column=0, pady=(5, 1))
        self.j_ci = Checkbutton(self, variable=self.jg_ci, onvalue=285, offvalue=300)
        self.j_ci.grid(row=1, column=0)
        self.m_ci = Checkbutton(self, variable=self.mid_ci, onvalue=285, offvalue=300)
        self.m_ci.grid(row=2, column=0)
        self.a_ci = Checkbutton(self, variable=self.ad_ci, onvalue=285, offvalue=300)
        self.a_ci.grid(row=3, column=0)
        self.s_ci = Checkbutton(self, variable=self.supp_ci, onvalue=285, offvalue=300)
        self.s_ci.grid(row=4, column=0)

        # Game Timer label + grid
        self.game_gui_label = Label(self, text="Game Timer:")
        self.game_gui_label.grid(row=6, column=3, ipadx=20)

        # Textbox to type in timer offset
        self.game_timer = Entry(self, width=10)
        self.game_timer.insert(END, '0')
        self.game_timer.grid(row=6, column=5, columnspan=3, pady=5)
        self.game_timer.bind("<Return>", self.retrieve_input)

        self.bind('<FocusOut>', self.start_sums)
        self.bind('<FocusIn>', self.on_focus)

        self.cb_final = ''

        self.rel_inp = 0

        # 1st temp set of roles (used later)
        self.temp_top = self.temp_jg = self.temp_mid = self.temp_ad = self.temp_supp = 0

        # 2nd temp set of roles (used later)
        self.t_top = self.t_jg = self.t_mid = self.t_ad = self.t_supp = ''

        # indiv. role strings to be appended to newest_iteration
        self.top_string = self.jg_string = self.mid_string = self.ad_string = self.supp_string = ''

        # buffer var to be checked w/ cb_final to allow mult roles to be printed in one action/line
        self.newest_iteration = ''

        # whether or not role's button is selected currently
        self.topBool = self.jgBool = self.midBool = self.adBool = self.suppBool = False

        # whether or not delay's button is selected currently
        self.add15Bool = self.add30Bool = self.add45Bool = False

        # keeps track whether summ is currently copied to "clipboard"
        self.t_copied = self.j_copied = self.m_copied = self.a_copied = self.s_copied = False

    # ALL 'swtch_foo()' methods are used to toggle state of its respective button. (probably refactor at some point)
    def swtch_top(self):
        if self.topBool:
            self.topBool = False
            self.tButton.configure(bg="SystemButtonFace")
        else:
            self.topBool = True
            self.tButton.configure(bg="green")

    def swtch_jg(self):
        if self.jgBool:
            self.jgBool = False
            self.jButton.configure(bg="SystemButtonFace")
        else:
            self.jgBool = True
            self.jButton.configure(bg="green")

    def swtch_mid(self):
        if self.midBool:
            self.midBool = False
            self.mButton.configure(bg="SystemButtonFace")
        else:
            self.midBool = True
            self.mButton.configure(bg="green")

    def swtch_ad(self):
        if self.adBool:
            self.adBool = False
            self.aButton.configure(bg="SystemButtonFace")
        else:
            self.adBool = True
            self.aButton.configure(bg="green")

    def swtch_supp(self):
        if self.suppBool:
            self.suppBool = False
            self.sButton.configure(bg="SystemButtonFace")
        else:
            self.suppBool = True
            self.sButton.configure(bg="green")

    def swtch15(self):
        if self.add15Bool:
            self.add15Bool = False
            self.add15Button.configure(bg="SystemButtonFace")
        else:
            self.add15Bool = True
            self.add15Button.configure(bg="green")
            if self.add30Bool:
                self.swtch30()
            if self.add45Bool:
                self.swtch45()

    def swtch30(self):
        if self.add30Bool:
            self.add30Bool = False
            self.add30Button.configure(bg="SystemButtonFace")
        else:
            self.add30Bool = True
            self.add30Button.configure(bg="green")
            if self.add15Bool:
                self.swtch15()
            if self.add45Bool:
                self.swtch45()

    def swtch45(self):
        if self.add45Bool:
            self.add45Bool = False
            self.add45Button.configure(bg="SystemButtonFace")
        else:
            self.add45Bool = True
            self.add45Button.configure(bg="green")
            if self.add15Bool:
                self.swtch15()
            if self.add30Bool:
                self.swtch30()

    # determines if any delay buttons are checked, and adds appropriate amount of delay to delay_list
    def apply_delay(self, index):
        if not self.add15Bool and not self.add30Bool and not self.add45Bool:
            self.delay_list[index] = 0
        elif self.add15Bool:
            self.delay_list[index] = 15
            self.add15Button.configure(bg="SystemButtonFace")
            self.add15Bool = False
        elif self.add30Bool:
            self.delay_list[index] = 30
            self.add30Button.configure(bg="SystemButtonFace")
            self.add30Bool = False
        elif self.add45Bool:
            self.delay_list[index] = 45
            self.add45Button.configure(bg="SystemButtonFace")
            self.add45Bool = False

    # is called whenever focus is lost on window,
    # if summ's button is active, its delay is applied, timer started, button color changed, and boolean reset
    def start_sums(self, event):
        if self.topBool:
            self.apply_delay(0)
            self.t_sw.restart()
            self.tButton.configure(bg="darkgray")
            self.topBool = False
        if self.jgBool:
            self.apply_delay(1)
            self.j_sw.restart()
            self.jButton.configure(bg="darkgray")
            self.jgBool = False
        if self.midBool:
            self.apply_delay(2)
            self.m_sw.restart()
            self.mButton.configure(bg="darkgray")
            self.midBool = False
        if self.adBool:
            self.apply_delay(3)
            self.a_sw.restart()
            self.aButton.configure(bg="darkgray")
            self.adBool = False
        if self.suppBool:
            self.apply_delay(4)
            self.s_sw.restart()
            self.sButton.configure(bg="darkgray")
            self.suppBool = False

    # is called whenever focus is gained on window,
    # flushes delay buttons' and unused/fresh summ's  colors to default,
    def on_focus(self, event):
        self.add15Button.configure(bg="SystemButtonFace")
        self.add30Button.configure(bg="SystemButtonFace")
        self.add45Button.configure(bg="SystemButtonFace")
        if self.t_sw.duration == 0.0:
            self.tButton.configure(bg="SystemButtonFace")
        if self.j_sw.duration == 0.0:
            self.jButton.configure(bg="SystemButtonFace")
        if self.m_sw.duration == 0.0:
            self.mButton.configure(bg="SystemButtonFace")
        if self.a_sw.duration == 0.0:
            self.aButton.configure(bg="SystemButtonFace")
        if self.s_sw.duration == 0.0:
            self.sButton.configure(bg="SystemButtonFace")

    # called when <Enter> button is pressed -> apply's given offset + starts game timer
    def retrieve_input(self, event):
        self.rel_inp = int(self.game_timer.get())
        self.game_sw.restart()

    # generalized method to add any summ
    def add_new_summ(self, role_index, temp_role, t_role, role_string, role_copied, role_name):
        temp_role = int(self.game_sw.duration + self.rel_inp - 1 + self.ci_list[role_index].get() - self.delay_list[role_index])
        if summ_rounder(t_role, temp_role) == '59':
            role_string = str((temp_role // 60) + 1) + role_name
        else:
            role_string = str(temp_role // 60) + summ_rounder(t_role, temp_role) + role_name
        if role_string[:-1 * len(role_name)] in self.newest_iteration:
            role_string = role_name
        self.newest_iteration += role_string
        role_copied = True
        return temp_role, t_role, role_string, role_copied, self.newest_iteration

    # used to add new summs by bringing up chat + typing out updated string + closing out of League's chat
    def prnt_scrpt(self):
        time.sleep(.25)

        # bringing up chat
        self.keyboard.press(kb.Key.enter)
        self.keyboard.press(kb.Key.enter)

        # typing timer(s)
        self.keyboard.type(self.cb_final)

        # selecting all
        self.keyboard.press(kb.Key.ctrl_l)
        time.sleep(.001)
        self.keyboard.press('a')
        self.keyboard.release('a')
        self.keyboard.release(kb.Key.ctrl_l)

        # copying all
        self.keyboard.press(kb.Key.ctrl_l)
        time.sleep(.001)
        self.keyboard.press('c')
        self.keyboard.release('c')
        self.keyboard.release(kb.Key.ctrl_l)

        # deleting all + esc'ing chat
        self.keyboard.press(kb.Key.ctrl_l)
        time.sleep(.001)
        self.keyboard.press('a')
        self.keyboard.release('a')
        self.keyboard.release(kb.Key.ctrl_l)
        time.sleep(.001)
        self.keyboard.press(kb.Key.delete)
        self.keyboard.release(kb.Key.delete)
        self.keyboard.press(kb.Key.enter)

    # used to delete old summs by bringing up chat + typing out updated string + closing out of League's chat
    def del_summs_scrpt(self):

        # bringing up chat
        self.keyboard.press(kb.Key.enter)
        self.keyboard.press(kb.Key.enter)

        # typing timer(s)
        self.keyboard.type(self.cb_final)

        # selecting all
        self.keyboard.press(kb.Key.ctrl_l)
        time.sleep(.001)
        self.keyboard.press('a')
        self.keyboard.release('a')
        self.keyboard.release(kb.Key.ctrl_l)

        # copying all
        self.keyboard.press(kb.Key.ctrl_l)
        time.sleep(.001)
        self.keyboard.press('c')
        self.keyboard.release('c')
        self.keyboard.release(kb.Key.ctrl_l)

        # deleting all + esc'ing chat
        self.keyboard.press(kb.Key.ctrl_l)
        time.sleep(.001)
        self.keyboard.press('a')
        self.keyboard.release('a')
        self.keyboard.release(kb.Key.ctrl_l)
        time.sleep(.01)
        self.keyboard.press(kb.Key.delete)
        self.keyboard.release(kb.Key.delete)
        self.keyboard.press(kb.Key.enter)


if __name__ == '__main__':

    # creating new Tk() object + setting size/location + adding icon
    root = Tk()
    w = 210
    h = 330
    x = (1920/2) - (w/2)
    y = (1080/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x+200, y-100))
    icon = ImageTk.PhotoImage(Image.open("extras/icon.ico"))
    root.iconphoto(False, icon)
    root.attributes('-alpha', 0.75)

    # tying Tk() object to our Window class above + flushing Checkbutton's states so they are "off"
    app = Window(root)
    app.t_ci.deselect()
    app.j_ci.deselect()
    app.m_ci.deselect()
    app.a_ci.deselect()
    app.s_ci.deselect()

    # Cycles constantly while program is running (maybe look at how to reduce memory/cpu usage here)
    while True:
        for i in range(len(app.summs_list)):

            # deletes expired summs from appropriate strings, updates in-game clipboard, plays audio cue, resets timers
            if app.summs_list[i].duration >= app.ci_list[i].get() - app.delay_list[i]:
                if i == 0:
                    app.cb_final, app.newest_iteration = app.cb_final.replace(app.top_string, ''), \
                                                         app.newest_iteration.replace(app.top_string, '')
                if i == 1:
                    app.cb_final, app.newest_iteration = app.cb_final.replace(app.jg_string, ''), \
                                                         app.newest_iteration.replace(app.jg_string, '')
                if i == 2:
                    app.cb_final, app.newest_iteration = app.cb_final.replace(app.mid_string, ''), \
                                                         app.newest_iteration.replace(app.mid_string, '')
                if i == 3:
                    app.cb_final, app.newest_iteration = app.cb_final.replace(app.ad_string, ''), \
                                                         app.newest_iteration.replace(app.ad_string, '')
                if i == 4:
                    app.cb_final, app.newest_iteration = app.cb_final.replace(app.supp_string, ''), \
                                                         app.newest_iteration.replace(app.mid_string, '')
                app.del_summs_scrpt()
                playsound(app.music_list[i])
                app.summs_list[i].reset()

            # allowing new summs/those that have just finished to be added onto the list
            if app.summs_list[i].duration == 0.0:
                if i == 0:
                    app.t_copied = False
                if i == 1:
                    app.j_copied = False
                if i == 2:
                    app.m_copied = False
                if i == 3:
                    app.a_copied = False
                if i == 4:
                    app.s_copied = False

            # adding new summs that are on cd to the list
            if app.summs_list[i].duration > 0.0:

                if i == 0 and app.t_copied is False:
                    app.temp_top, app.t_top, app.top_string, app.t_copied, app.newest_iteration =     \
                                   app.add_new_summ(0, app.temp_top, app.t_top, app.top_string, app.t_copied, 'top ')

                if i == 1 and app.j_copied is False:
                    app.temp_jg, app.t_jg, app.jg_string, app.j_copied, app.newest_iteration =     \
                                   app.add_new_summ(1, app.temp_jg, app.t_jg, app.jg_string, app.j_copied, 'jg ')

                if i == 2 and app.m_copied is False:
                    app.temp_mid, app.t_mid, app.mid_string, app.m_copied, app.newest_iteration =     \
                                   app.add_new_summ(2, app.temp_mid, app.t_mid, app.mid_string, app.m_copied, 'mid ')

                if i == 3 and app.a_copied is False:
                    app.temp_ad, app.t_ad, app.ad_string, app.a_copied, app.newest_iteration =     \
                                   app.add_new_summ(3, app.temp_ad, app.t_ad, app.ad_string, app.a_copied, 'ad ')

                if i == 4 and app.s_copied is False:
                    app.temp_supp, app.t_supp, app.supp_string, app.s_copied, app.newest_iteration =     \
                                   app.add_new_summ(4, app.temp_supp, app.t_supp, app.supp_string, app.s_copied, 'sup ')

        # used to reduce redundancy when timing multiple flashes at once -> types them out on one line
        if app.newest_iteration != app.cb_final:
            app.cb_final = app.newest_iteration
            app.prnt_scrpt()

        # keeps program up to date while in a loop like this
        root.update_idletasks()
        root.update()
