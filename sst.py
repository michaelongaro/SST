from tkinter import *
from playsound import playsound
from stopwatch import Stopwatch
import pynput.keyboard as kb
import pynput.mouse as ms
from PIL import ImageTk, Image
import time

# cb_final values into the overlay (still to be made)
# "unused" vars in add_new_summ()

# think about realistic situations on whether adding +5 to man timers are useful or not

# lets just look at sub 5 min timers for a lil bit, hopefully easy sheet

def summ_rounder(t_var, other):
    if 55 <= other % 60 <= 59:
        t_var = '59'
    elif 0 <= other % 60 <= 4:
        t_var = ''
    elif 5 <= other % 60 < 15:
        t_var = '10'
    elif 16 <= other % 60 < 25:
        t_var = '20'
    elif 26 <= other % 60 < 35:
        t_var = '30'
    elif 36 <= other % 60 < 45:
        t_var = '40'
    elif 46 <= other % 60 < 54:
        t_var = '50'
    return t_var

def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb

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
        self.t_sw = Stopwatch().reset()
        self.j_sw = Stopwatch().reset()
        self.m_sw = Stopwatch().reset()
        self.a_sw = Stopwatch().reset()
        self.s_sw = Stopwatch().reset()

        # vars to store ss cds for CheckButtons
        self.top_ci = IntVar(master)
        self.jg_ci = IntVar(master)
        self.mid_ci = IntVar(master)
        self.ad_ci = IntVar(master)
        self.supp_ci = IntVar(master)

        # how many seconds each role's timer is when called
        self.topExactSecs = 0
        self.jgExactSecs = 0
        self.midExactSecs = 0
        self.adExactSecs = 0
        self.suppExactSecs = 0

        self.summs_list = [self.t_sw, self.j_sw, self.m_sw, self.a_sw, self.s_sw]
        self.ci_list = [self.top_ci, self.jg_ci, self.mid_ci, self.ad_ci, self.supp_ci]

        self.exactRoleSecs = [self.topExactSecs, self.jgExactSecs, self.midExactSecs, self.adExactSecs, self.suppExactSecs]

        self.music_list = ['extras/top.mp3', 'extras/jg.mp3', 'extras/mid.mp3', 'extras/ad.mp3', 'extras/supp.mp3']

        self.top_img = ImageTk.PhotoImage(Image.open("extras/top.png"))
        self.jg_img = ImageTk.PhotoImage(Image.open("extras/jg.png"))
        self.mid_img = ImageTk.PhotoImage(Image.open("extras/mid.png"))
        self.ad_img = ImageTk.PhotoImage(Image.open("extras/ad.png"))
        self.supp_img = ImageTk.PhotoImage(Image.open("extras/supp.png"))

        self.ci_img = ImageTk.PhotoImage(Image.open("extras/ci.png"))

        # Individual Role Buttons + images + placing them on grid
        self.tButton = Button(self, height=50, image=self.top_img, command=self.swtch_top)
        self.tButton.image = self.top_img
        self.tButton.grid(row=0, column=1, columnspan=3, sticky=W+E, padx=5, pady=(5, 1))

        self.jButton = Button(self, width=10, height=50, image=self.jg_img, command=self.swtch_jg)
        self.jButton.image = self.jg_img
        self.jButton.grid(row=1, column=1, columnspan=3, sticky=W+E, padx=5, pady=1)

        self.mButton = Button(self, width=10, height=50, image=self.mid_img, command=self.swtch_mid)
        self.mButton.image = self.mid_img
        self.mButton.grid(row=2, column=1, columnspan=3, sticky=W+E, padx=5, pady=1)

        self.aButton = Button(self, width=10, height=50, image=self.ad_img, command=self.swtch_ad)
        self.aButton.image = self.ad_img
        self.aButton.grid(row=3, column=1, columnspan=3, sticky=W+E, padx=5, pady=1)

        self.sButton = Button(self, width=10, height=50, image=self.supp_img, command=self.swtch_supp)
        self.sButton.image = self.supp_img
        self.sButton.grid(row=4, column=1, columnspan=3, sticky=W+E, padx=5)

        self.buttonList = [self.tButton, self.jButton, self.mButton, self.aButton, self.sButton]
        # Specific timer(s) for each role (to be entered manually)

        self.manTopField = Entry(self, width=10)
        self.manTopField.insert(END, '')
        self.manTopField.grid(row=0, column=6, columnspan=2, sticky=E, pady=(5, 1))
        self.manJgField = Entry(self, width=10)
        self.manJgField.insert(END, '')
        self.manJgField.grid(row=1, column=6, columnspan=2, sticky=E, pady=(5, 1))
        self.manMidField = Entry(self, width=10)
        self.manMidField.insert(END, '')
        self.manMidField.grid(row=2, column=6, columnspan=2, sticky=E, pady=(5, 1))
        self.manAdField = Entry(self, width=10)
        self.manAdField.insert(END, '')
        self.manAdField.grid(row=3, column=6, columnspan=2, sticky=E, pady=(5, 1))
        self.manSuppField = Entry(self, width=10)
        self.manSuppField.insert(END, '')
        self.manSuppField.grid(row=4, column=6, columnspan=2, sticky=E, pady=(5, 1))

        self.delay_list = [self.manTopField.get(), self.manJgField.get(), self.manMidField.get(),
                           self.manAdField.get(), self.manSuppField.get()]
        self.entryList = [self.manTopField, self.manJgField, self.manMidField, self.manAdField, self.manSuppField]

        # Cosmic Insight Checkbuttons (for each role) + ci icon + placing them on grid
        self.t_ci = Checkbutton(self, variable=self.top_ci, onvalue=285, offvalue=300)
        self.t_ci.grid(row=0, column=0, pady=(5, 1), padx=1)
        self.j_ci = Checkbutton(self, variable=self.jg_ci, onvalue=285, offvalue=300)
        self.j_ci.grid(row=1, column=0, padx=1)
        self.m_ci = Checkbutton(self, variable=self.mid_ci, onvalue=285, offvalue=300)
        self.m_ci.grid(row=2, column=0, padx=1)
        self.a_ci = Checkbutton(self, variable=self.ad_ci, onvalue=285, offvalue=300)
        self.a_ci.grid(row=3, column=0, padx=1)
        self.s_ci = Checkbutton(self, variable=self.supp_ci, onvalue=285, offvalue=300)
        self.s_ci.grid(row=4, column=0, padx=1)

        self.ci_image = Label(self, image=self.ci_img)
        self.ci_image.image = self.ci_image
        self.ci_image.grid(row=6, column=0, sticky=W)

        # Game Timer label + grid
        self.game_gui_label = Label(self, text="Game Timer:")
        self.game_gui_label.grid(row=6, column=3, ipadx=20)

        # Textbox to type in timer offset
        self.game_timer = Entry(self, width=10)
        self.game_timer.insert(END, '')
        self.game_timer.grid(row=6, column=5, columnspan=3, pady=10)
        self.game_timer.bind("<Return>", self.retrieve_input)

        self.bind('<FocusOut>', self.start_sums)
        self.bind('<FocusIn>', self.on_focus)

        # Clipboard_final = final string to be "copied" and printed out to the screen
        self.cb_final = ''

        # game timer offset provided by the user
        self.rel_inp = 0

        # 1st temp set of roles (used later)
        self.temp_top = 0
        self.temp_jg = 0
        self.temp_mid = 0
        self.temp_ad = 0
        self.temp_supp = 0

        # 2nd temp set of roles (used later)
        self.t_top = ''
        self.t_jg = ''
        self.t_mid = ''
        self.t_ad = ''
        self.t_supp = ''

        # indiv. role strings to be appended to newest_iteration
        self.top_string = ''
        self.jg_string = ''
        self.mid_string = ''
        self.ad_string = ''
        self.supp_string = ''

        # buffer var to be checked w/ cb_final to allow mult roles to be printed in one action/line
        self.newest_iteration = ''

        # whether or not role's button is selected currently
        self.topBool = False
        self.jgBool = False
        self.midBool = False
        self.adBool = False
        self.suppBool = False

        # keeps track whether summ is currently copied to "clipboard"
        self.t_copied = False
        self.j_copied = False
        self.m_copied = False
        self.a_copied = False
        self.s_copied = False

        self.t_valid = False
        self.j_valid = False
        self.m_valid = False
        self.a_valid = False
        self.s_valid = False

        self.manValidList = [self.t_valid, self.j_valid, self.m_valid, self.a_valid, self.s_valid]

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

    # ========= Any "event" param added below necessary because the function calling it is passing a value =============

    # is called whenever focus is lost on window,
    # if summ's button is active, its delay is applied, timer started, button color changed, and boolean reset
    def start_sums(self, event):
        # eventually make this so that it will allow the default to be a blank entry field w/o needing 0
        # pretty low prio tbh

        # ALSO try and get summs to be printed out in order of which comes up first

        # ALSO need to copypasta da mechs to allow game timer to be written as mmss

        # ALSO need to figure out eventually how to get api to figure out whether or not CI is present


        # have a lil error handling section here! try and catch, if catch just pass it i believe
        # maybe need to lookup what the error name was (eeek! that means you will have to willingly let ur code break!)
        for q in range(len(self.delay_list)):

            try:
                self.delay_list[q] = int(self.entryList[q].get())
            except ValueError:
                self.manValidList[q] = False
            else:
                self.manValidList[q] = True

        #self.delay_list[0] = int(self.manTopField.get())
        #self.delay_list[1] = int(float(self.manJgField.get()))
        #self.delay_list[2] = int(float(self.manMidField.get()))
        #self.delay_list[3] = int(float(self.manAdField.get()))
        #self.delay_list[4] = int(float(self.manSuppField.get()))

        if self.topBool:
            self.t_sw.restart()
            self.tButton.configure(bg="SystemButtonFace")
            self.tButton["state"] = "disabled"
            self.topBool = False
            self.exactRoleSecs[0] = self.ci_list[0].get()
        elif self.manValidList[0] and self.t_sw.duration == 0:
            self.t_sw.restart()
            self.tButton.configure(bg="SystemButtonFace")
            self.tButton["state"] = "disabled"
            self.topBool = False
            self.exactRoleSecs[0] = int(self.delay_list[0] % 100 + (self.delay_list[0] // 100) * 60)\
                                 - int(self.game_sw.duration + self.rel_inp)

        if self.jgBool:
            self.j_sw.restart()
            self.jButton.configure(bg="SystemButtonFace")
            self.jButton["state"] = "disabled"
            self.jgBool = False
            self.exactRoleSecs[1] = self.ci_list[1].get()
        elif self.manValidList[1] and self.j_sw.duration == 0:
            self.j_sw.restart()
            self.jButton.configure(bg="SystemButtonFace")
            self.jButton["state"] = "disabled"
            self.jgBool = False
            self.exactRoleSecs[1] = int(self.delay_list[1] % 100 + (self.delay_list[1] // 100) * 60)\
                                 - int(self.game_sw.duration + self.rel_inp)

        if self.midBool:
            self.m_sw.restart()
            self.mButton.configure(bg="SystemButtonFace")
            self.mButton["state"] = "disabled"
            self.midBool = False
            self.exactRoleSecs[2] = self.ci_list[2].get()
        elif self.manValidList[2] and self.m_sw.duration == 0:
            self.m_sw.restart()
            self.mButton.configure(bg="SystemButtonFace")
            self.mButton["state"] = "disabled"
            self.midBool = False
            self.exactRoleSecs[2] = int(self.delay_list[2] % 100 + (self.delay_list[2] // 100) * 60)\
                                 - int(self.game_sw.duration + self.rel_inp)

        if self.adBool:
            self.a_sw.restart()
            self.aButton.configure(bg="SystemButtonFace")
            self.aButton["state"] = "disabled"
            self.adBool = False
            self.exactRoleSecs[3] = self.ci_list[3].get()
        elif self.manValidList[3] and self.a_sw.duration == 0:
            self.a_sw.restart()
            self.aButton.configure(bg="SystemButtonFace")
            self.aButton["state"] = "disabled"
            self.adBool = False
            self.exactRoleSecs[3] = int(self.delay_list[3] % 100 + (self.delay_list[3] // 100) * 60)\
                                 - int(self.game_sw.duration + self.rel_inp)

        if self.suppBool:
            self.s_sw.restart()
            self.sButton.configure(bg="SystemButtonFace")
            self.sButton["state"] = "disabled"
            self.suppBool = False
            self.exactRoleSecs[4] = self.ci_list[4].get()
        elif self.manValidList[4] and self.s_sw.duration == 0:
            self.s_sw.restart()
            self.sButton.configure(bg="SystemButtonFace")
            self.sButton["state"] = "disabled"
            self.suppBool = False
            self.exactRoleSecs[4] = int(self.delay_list[4] % 100 + (self.delay_list[4] // 100) * 60)\
                                 - int(self.game_sw.duration + self.rel_inp)

    # is called whenever focus is gained on window,
    # flushes delay buttons' and unused/fresh summ's  colors to default,
    def on_focus(self, event):
        for role in range(len(self.summs_list)):
            if self.summs_list[role].duration > 0.0:
                self.entryList[role].delete(0, 'end')
                self.entryList[role].insert(0, str(int(self.exactRoleSecs[role] - self.summs_list[role].duration)))

                # red
                if (self.exactRoleSecs[role] - self.summs_list[role].duration) > 200:
                    self.entryList[role].config(background=_from_rgb((255, 0, 0)))
                # orange
                elif 200 >= (self.exactRoleSecs[role] - self.summs_list[role].duration) > 100:
                    self.entryList[role].config(background=_from_rgb((255, 100, 0)))
                # yellow
                elif 100 >= (self.exactRoleSecs[role] - self.summs_list[role].duration) > 0:
                    self.entryList[role].config(background=_from_rgb((255, 255, 0)))

            #print(self.summs_list[role].duration)
            ## green(s)
            #if self.summs_list[role] == 0.0:
            #    print('reached')
            #    self.buttonList[role]["state"] = "normal"
            #    self.entryList[role].config(background=_from_rgb((0, 255, 0)))
            #    print('reached2')

    # called when <Enter> button is pressed -> apply's given offset + starts game timer
    def retrieve_input(self, event):
        # make this adaptive based off of number of digits
        self.rel_inp = int(self.game_timer.get())
        self.game_sw.restart()
        print(self.rel_inp)

    # generalized method to add any summ
    def add_new_summ(self, role_index, temp_role, t_role, role_string, role_copied, role_name):
        temp_role = int(self.game_sw.duration + self.rel_inp - 1 + self.exactRoleSecs[role_index])

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
        time.sleep(.15)

        # bringing up chat
        self.keyboard.tap(kb.Key.enter)

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
        time.sleep(.001)
        self.keyboard.press(kb.Key.delete)
        self.keyboard.release(kb.Key.delete)
        self.keyboard.tap(kb.Key.enter)

        time.sleep(.15)
        # POTENTIALLY: look into why sometimes when two summs are same timer and timed back-to-back,
        # both audio cues dont go off before sums are deleted. Could just be due to difference in length
        # of the mp3 files. worth a check tho
if __name__ == '__main__':

    # creating new Tk() object + setting size/location + adding icon
    root = Tk()
    w = 230
    h = 330
    x = (1920/2) - (w/2)
    y = (1080/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x+200, y-100))
    icon = ImageTk.PhotoImage(Image.open("extras/icon.ico"))
    root.iconphoto(False, icon)
    root.attributes('-alpha', 0.75)

    x = True

    def update_x():
        global x
        x = False


    root.protocol("WM_DELETE_WINDOW", update_x)

    # tying Tk() object to our Window class above + flushing Checkbutton's states so they are "off"
    app = Window(root)
    app.t_ci.deselect()
    app.j_ci.deselect()
    app.m_ci.deselect()
    app.a_ci.deselect()
    app.s_ci.deselect()

    # Cycles constantly while program is running (maybe look at how to reduce memory/cpu usage here)
    while x:
        for i in range(len(app.summs_list)):

            # deletes expired summs from appropriate strings, updates in-game clipboard, plays audio cue, resets timers
            # and any other miscellaneous values to zero
            if app.summs_list[i].duration > app.exactRoleSecs[i]:
                if i == 0:
                    app.newest_iteration = app.newest_iteration.replace(app.top_string, '')
                if i == 1:
                    app.newest_iteration = app.newest_iteration.replace(app.jg_string, '')
                if i == 2:
                    app.newest_iteration = app.newest_iteration.replace(app.mid_string, '')
                if i == 3:
                    app.newest_iteration = app.newest_iteration.replace(app.ad_string, '')
                if i == 4:
                    app.newest_iteration = app.newest_iteration.replace(app.supp_string, '')

                app.entryList[i].delete(0, 'end')
                app.entryList[i].insert(END, '')
                app.exactRoleSecs[i] = 0

                playsound(app.music_list[i])
                app.summs_list[i].reset()

                app.buttonList[i]["state"] = "normal"
                app.entryList[i].config(background=_from_rgb((255, 255, 255)))

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

        # pushes any changes staged previously in newest_iteration to cb_final
        # also: used to reduce redundancy when adding/deleting multiple flashes at once -> types them out on one line
        if app.newest_iteration != app.cb_final:
            app.cb_final = app.newest_iteration
            app.prnt_scrpt()

        # keeps program up to date while in a loop like this*
        root.update_idletasks()
        root.update()
