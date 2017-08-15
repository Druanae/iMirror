#!/usr/bin/env python
from tkinter import *

class BuildGUI:
    def __init__(self):
        self.root = Tk()
        self.left_frame = Frame(self.root, background="black")
        self.left_frame.pack(side=LEFT, fill=BOTH, expand=YES)
        self.right_frame = Frame(self.root, background="white")
        self.right_frame.pack(side=RIGHT, fill=BOTH, expand=YES)

if __name__ == "__main__":
    WINDOW = BuildGUI()
    WINDOW.root.mainloop()
