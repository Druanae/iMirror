#!/usr/bin/env python
import feedparser
import traceback

class Newsfeed():
    def __init__(self):
        self.headlines = []
        self.GetNews()

    def GetNews(self):
        try:
            # get XML data from BBC
            news_url = "http://feeds.bbci.co.uk/news/uk/rss.xml"
            feed = feedparser.parse(news_url)

            i = 0
            for item in feed.entries[0:5]:
                self.headlines.insert(i, item.title)
                i += 1

        except Exception as e:
            traceback.print_exc()
            print ("Error: %s. Cannot get news." % e)


n = Newsfeed()
for i in range(0, len(n.headlines)):
    print("Headline %s: %s" % (i+1,  n.headlines[i]))
