#!/usr/bin/env python
from tkinter import *
from traceback import print_exc
from feedparser import parse

XL_TEXT = 94
LG_TEXT = 48
MD_TEXT = 28
SM_TEXT = 18

class Test(Frame):
    def __init__(self, parent):
        
        Frame.__init__(self, parent)
        self.config(bg='black')
        self.title= 'News'
        self.news_label = Label(self, text=self.title, \
                                font=('Lato', MD_TEXT), \
                                fg='white', bg='black')
        self.news_label.pack(side=TOP, anchor=E)
        self.headlines_label = Label(self, font=('Lato', SM_TEXT), \
                                     fg='white', bg='black')
        self.headlines_label.pack(side=TOP, anchor=E)

        self.get_news()

    def get_news(self):
        try:
            news_url = "http://feeds.bbci.co.uk/news/uk/rss.xml"
            feed = parse(news_url)
            headlines = []
            index = 0
            for item in feed.entries[0:5]:
                headlines_tmp.insert(index, item.title)
                index += 1

            headlines_tmp = '\n'.join(headlines)
            self.headlines_label.config(text=headlines)

        except Exception as exc:
            print_exc()
            print("Error %s. Cannot get news." % exc)


class BuildGUI():
    def __init__(self):
        self.root = Tk()
        self.root.config(background='black')
        self.frame = Frame(self.root, background='black')
        self.frame.pack(side=TOP, fill=BOTH, expand=YES)
        self.state = False

        self.test = Test(self.frame)
        self.test.pack(side=LEFT, anchor=N, padx=50, pady=50)

if __name__ == "__main__":
    WINDOW = BuildGUI()
    WINDOW.root.mainloop()
