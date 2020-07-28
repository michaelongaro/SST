from tkinter import *
from playsound import playsound
from stopwatch import Stopwatch
import pynput.keyboard as kb
import pynput.mouse as ms
from PIL import ImageTk,Image
import time

# still needs testing, seems like it only works sometimes when its tabbing back in
# honestly idk what this correlation is but when you do top + mid at same time, it
# ^ maybe fixed. prob want to add an offset timer where you can type in 30 or some shit and it fixes stuff for you!

# how to stop it from locking you in chat(?) i guess is what is happening
# make the timers actually work (aka bump the timers back)
# prob add 5 checkboxes for cosmic insight and shorten name to "CI:"
# can add as many row/cols as you want just span the bastards to whatever length you need
# you can and should 100% refactor this code, its straight up an eyesore to look at

# why does it insta start q'ing up all roles sounds

# SHOULD probably make all top through supp vars into lists and go off of index (assuming they are declared with the same vars)
# BIG issue btw! -> after deleting summs (and tabbing out to time them again quickly i think is the big thing?),
#                   it records the first summ, but glitches out on the second. I believe the chat is still open at the end

# potential solut9ion: add a left click after the tab back in to bring to focus

# what is reasonable scenario here: alt-tab back into league,
                                #   opens chat, types ad thing, closes chat
                                #   bugs on opening chat here?, types anyway, opens chat
                                #       maybe look into how hard it would be to make same time timers one action to make + delete
                                #       could be a cool loophole1

# make it so roles that have active timers have darker backgrounds for the buttons, pretty simple

# this was potentially defined as a static method, what is that and why would that be an issue. was def inside class b4
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

    def prnt_scrpt(self):
        time.sleep(.25)

        # bringing up chat
        self.keyboard.press(kb.Key.enter)
        self.keyboard.press(kb.Key.enter)
        #time.sleep(.001)
        #self.keyboard.release(kb.Key.enter)

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
        #time.sleep(.001)
        #self.keyboard.release(kb.Key.enter)
        #time.sleep(.001)

    def del_summs_scrpt(self):

        # bringing up chat
        self.keyboard.press(kb.Key.enter)
        self.keyboard.press(kb.Key.enter)
        #time.sleep(.001)
        #self.keyboard.release(kb.Key.enter)

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
        #time.sleep(.001)
        #self.keyboard.release(kb.Key.enter)

    def __init__(self, master):
        Frame.__init__(self, master)

        self.master = master

        self.master.title("SST")

        self.pack()

        self.t_sw = Stopwatch().reset()
        self.j_sw = Stopwatch().reset()
        self.m_sw = Stopwatch().reset()
        self.a_sw = Stopwatch().reset()
        self.s_sw = Stopwatch().reset()

        # i guess you need to declare these afterthe root=Tk() statement, weird, think of clear way to do this?
        # just instantiate these vars up here, no declaration, and then add the IntVars on in the main method.

        self.top_ci = IntVar(master)
        self.jg_ci = IntVar(master)
        self.mid_ci = IntVar(master)
        self.ad_ci = IntVar(master)
        self.supp_ci = IntVar(master)

        self.summs_list = [self.t_sw, self.j_sw, self.m_sw, self.a_sw, self.s_sw]
        self.ci_list = [self.top_ci, self.jg_ci, self.mid_ci, self.ad_ci, self.supp_ci]
        self.delay_list = [0, 0, 0, 0, 0]
        self.music_list = ['extras/top.mp3', 'extras/jg.mp3', 'extras/mid.mp3', 'extras/ad.mp3', 'extras/supp.mp3']

        top_img = ImageTk.PhotoImage(Image.open("extras/top.png"))
        jg_img = ImageTk.PhotoImage(Image.open("extras/jg.png"))
        mid_img = ImageTk.PhotoImage(Image.open("extras/mid.png"))
        ad_img = ImageTk.PhotoImage(Image.open("extras/ad.png"))
        supp_img = ImageTk.PhotoImage(Image.open("extras/supp.png"))

        # maybe figure out why the scaling on this is so weird
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

        #self.cosmic_gui_label = Label(self, text="CI:", width=1)
        #self.cosmic_gui_label.grid(row=5, column=0)

        self.add15Button = Button(self, width=8, height=3, text="+15", command=self.swtch15)
        self.add15Button.grid(row=0, column=6, columnspan=2, sticky=E, pady=(5, 1))
        self.add30Button = Button(self, width=8, height=3, text="+30", command=self.swtch30)
        self.add30Button.grid(row=2, column=6, columnspan=2, sticky=E, pady=1)
        self.add45Button = Button(self, width=8, height=3, text="+45", command=self.swtch45)
        self.add45Button.grid(row=4, column=6, columnspan=2, sticky=E, pady=1)

        # ci stuff (change here)
        self.t_ci = Checkbutton(self, variable=self.top_ci, onvalue=285, offvalue=300)
        self.t_ci.grid(row=0, column=0, pady=(5,1))
        self.j_ci = Checkbutton(self, variable=self.jg_ci, onvalue=285, offvalue=300)
        self.j_ci.grid(row=1, column=0)
        self.m_ci = Checkbutton(self, variable=self.mid_ci, onvalue=285, offvalue=300)
        self.m_ci.grid(row=2, column=0)
        self.a_ci = Checkbutton(self, variable=self.ad_ci, onvalue=285, offvalue=300)
        self.a_ci.grid(row=3, column=0)
        self.s_ci = Checkbutton(self, variable=self.supp_ci, onvalue=285, offvalue=300)
        self.s_ci.grid(row=4, column=0)

        self.game_sw = Stopwatch()

        self.cb_final = ''

        self.t_copied = False
        self.j_copied = False
        self.m_copied = False
        self.a_copied = False
        self.s_copied = False

        self.game_gui_label = Label(self, text="Game Timer:")
        self.game_gui_label.grid(row=6, column=3, ipadx=20)

        self.actual_game_time = 0

        # BIG BRAIN maybe: the column/row size is defined by the smallest element in that col/row

        self.game_timer = Entry(self, width=10)
        self.game_timer.insert(END, '0')
        self.game_timer.grid(row=6, column=5, columnspan=3, pady=5)
        self.game_timer.bind("<Return>", self.retrieve_input)

        #self.delay_val = Entry(self, width=5)
        #self.delay_val.insert(END, '0')
        #self.delay_val.grid(row=6, column=2, padx=5, pady=5)
        #self.delay_val.bind("<Return>", self.update_delay_offset)

        self.bind('<FocusOut>', self.start_sums)
        self.bind('<FocusIn>', self.on_focus)

        self.rel_inp = 0

        self.temp_top = 0
        self.temp_jg = 0
        self.temp_mid = 0
        self.temp_ad = 0
        self.temp_supp = 0

        self.t_top = ''
        self.t_jg = ''
        self.t_mid = ''
        self.t_ad = ''
        self.t_supp = ''

        self.keyboard = kb.Controller()
        self.mouse = ms.Controller()

        self.top_string = ''
        self.jg_string = ''
        self.mid_string = ''
        self.ad_string = ''
        self.supp_string = ''

        self.newest_iteration = ''

        # whether or not button is selected currently
        self.topBool = False
        self.jgBool = False
        self.midBool = False
        self.adBool = False
        self.suppBool = False

        self.add15Bool = False
        self.add30Bool = False
        self.add45Bool = False

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


    def retrieve_input(self, event):
        self.rel_inp = int(self.game_timer.get())
        self.game_sw.restart()

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


if __name__ == '__main__':

    root = Tk()
    w = 210
    h = 330
    x = (1920/2) - (w/2)
    y = (1080/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x+200, y-100))
    icon = ImageTk.PhotoImage(Image.open("extras/icon.ico"))
    root.iconphoto(False, icon)
    root.attributes('-alpha', 0.75)

    app = Window(root)
    app.t_ci.deselect()
    app.j_ci.deselect()
    app.m_ci.deselect()
    app.a_ci.deselect()
    app.s_ci.deselect()

    while True:
        for i in range(len(app.summs_list)):

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

            # ALLOWING NEW SUMMS/THOSE THAT HAVE JUST FINISHED TO BE ADDED ONTO THE LIST
            #print('before potential reset: ', app.a_copied, app.s_copied)
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

            # ADDING NEW SUMMS THAT ARE ON CD TO THE LIST
            if app.summs_list[i].duration > 0.0:
                # SERIOUSLY look into scoping and try to deeply understand concept behind it + applications
                if i == 0 and app.t_copied is False:
                    app.temp_top, app.t_top, app.top_string, app.t_copied, app.newest_iteration = app.add_new_summ(0, app.temp_top, app.t_top, app.top_string, app.t_copied, 'top ')
                # temp_role, t_role, role_string, role_copied, role_name
                if i == 1 and app.j_copied is False:
                    app.temp_jg, app.t_jg, app.jg_string, app.j_copied, app.newest_iteration = app.add_new_summ(1, app.temp_jg, app.t_jg, app.jg_string, app.j_copied, 'jg ')

                if i == 2 and app.m_copied is False:
                    app.temp_mid, app.t_mid, app.mid_string, app.m_copied, app.newest_iteration = app.add_new_summ(2, app.temp_mid, app.t_mid, app.mid_string, app.m_copied, 'mid ')

                if i == 3 and app.a_copied is False:
                    app.temp_ad, app.t_ad, app.ad_string, app.a_copied, app.newest_iteration = app.add_new_summ(3, app.temp_ad, app.t_ad, app.ad_string, app.a_copied, 'ad ')

                if i == 4 and app.s_copied is False:
                    app.temp_supp, app.t_supp, app.supp_string, app.s_copied, app.newest_iteration = app.add_new_summ(4, app.temp_supp, app.t_supp, app.supp_string, app.s_copied, 'sup ')

                #print(app.newest_iteration)

        # this doesnt work, figure out why 

        if app.newest_iteration != app.cb_final:
            app.cb_final = app.newest_iteration
            app.prnt_scrpt()

        root.update_idletasks()
        root.update()
