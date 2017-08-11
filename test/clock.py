#!/usr/bin/env python
import time
import locale
import threading
from contextlib import contextmanager
from tkinter import *

# Locale and time settings
LOCALE_LOCK = threading.Lock()

UI_LOCALE = 'en_GB.utf-8'
TIME_FORMAT = None
DATE_FORMAT = "%b %d, %Y"

# Tkinter constants
XL_TEXT = 94
LG_TEXT = 48
MD_TEXT = 28
SM_TEXT = 18

@contextmanager
def setlocale(name):
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)

class Clock(Frame):
    def __init__(self, parent, *args, **kwargs):
        self.time = ''
        self.day = ''
        self.date = ''

        Frame.__init__(self, parent, bg='black')
        self.time_label = Label(self, font=('Lato', LG_TEXT),\
            fg="white", bg="black")
        self.time_label.pack(side=TOP, anchor=E)

        self.date_label = Label(self, font=('Lato', SM_TEXT),\
            fg="white", bg="black")
        self.date_label.pack(side=TOP, anchor=E)

        self.day_label = Label(self, font=('Lato', SM_TEXT),\
            fg="white", bg="black")
        self.day_label.pack(side=TOP, anchor=E)
        self.tick()

    def tick(self):
        with setlocale(UI_LOCALE):
            if TIME_FORMAT == 12:
                time_tmp = time.strftime('%I:%M %p')
            else:
                time_tmp = time.strftime('%H:%M')

            day_tmp = time.strftime('%A')
            date_tmp = time.strftime(DATE_FORMAT)

            if time_tmp != self.time:
                self.time = time_tmp
                self.time_label.config(text=time_tmp)
            if day_tmp != self.day:
                self.day = day_tmp
                self.day_label.config(text=day_tmp)
            if date_tmp != self.date:
                self.date = date_tmp
                self.date_label.config(text=date_tmp)

            self.time_label.after(200, self.tick)


class BuildGUI:

    def __init__(self):
        self.tk = Tk()
        self.tk.configure(background='black')
        self.topFrame = Frame(self.tk, background = 'black')
        self.bottomFrame = Frame(self.tk, background = 'black')
        self.topFrame.pack(side = TOP, fil=BOTH, expand = YES)
        self.bottomFrame.pack(side = BOTTOM, fill = BOTH, expand = YES)
        self.state = False
        self.tk.bind("<Return>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)

        #clock
        self.clock = Clock(self.topFrame)
        self.clock.pack(side=RIGHT, anchor=N, padx=50, pady = 30)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"

if __name__ == "__main__":
    w = BuildGUI()
    w.tk.mainloop()
