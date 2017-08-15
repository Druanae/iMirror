#!/usr/bin/env python
"""
News GUI Test Script
"""

import tkinter as tk
from traceback import print_exc
from feedparser import parse

XL_TEXT = 94
LG_TEXT = 48
MD_TEXT = 28
SM_TEXT = 18

class News(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.config(bg='black')
        self.title = 'News'
        self.news_label = tk.Label(self, text=self.title, \
                                   font=('Lato', MD_TEXT), \
                                   fg='white', bg='black')
        self.news_label.pack(side=tk.TOP, anchor=tk.E)
        self.headlines_label = tk.Label(self, font=('Lato', SM_TEXT), \
                              fg='white', bg='black')
        self.headlines_label.pack(side=tk.TOP, anchor=tk.E)

        self.get_news()

    def get_news(self):
        """
        get_news class
        fetches XML data from the BBC using feedparser
        """

        try:
            # reset headline info in headline_container
            self.headlines_label.config(text="")
            
            ### Fetch XML data from news website ###
            # store XML url in variable
            news_url = "http://feeds.bbci.co.uk/news/uk/rss.xml"
            # parse XML data into Python object and store in variable
            feed = parse(news_url)
            # store headlines in array
            headlines = []
            # iterate through XML and store first 5 headlines in self.headlines
            index = 0
            for item in feed.entries[0:5]:
                # create child widgets containing
                headlines.insert(index, item.title)
                index += 1

            headlines = '\n'.join(headlines)
            self.headlines_label.config(text=headlines)

        except Exception as exc:
            print_exc()
            print("Error %s. Cannot get news." % exc)

        self.after(600000, self.get_news)

class BuildGUI():
    def __init__(self):
        self.tk = tk.Tk()
        self.tk.config(background='black')
        self.top_frame = tk.Frame(self.tk, background='black')
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
        self.bottom_frame = tk.Frame(self.tk, background='black')
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.YES)
        self.state = False

        self.news = News(self.bottom_frame)
        self.news.pack(side=tk.LEFT, anchor=tk.N, padx=50, pady=50)
        self.news.headlines_label.config(justify=tk.RIGHT)

if __name__ == "__main__":
    WINDOW = BuildGUI()
    WINDOW.tk.mainloop()
