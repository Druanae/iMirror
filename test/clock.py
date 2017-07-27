#!/usr/bin/env python
import time
import locale
import threading
from contextlib import contextmanager

LOCALE_LOCK = threading.Lock()

UI_LOCALE = ''
TIME_FORMAT = 12
DATE_FORMAT = "%b %d, %Y"

@contextmanager
def setlocale(name):
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)

class Clock:
    def __init__(self, *args, **kwargs):
        self.time1 = ''
        self.day_of_week1 = ''
        self.date1 = ''
        self.tick()

    def tick(self):
        with setlocale(UI_LOCALE):
            if TIME_FORMAT == 12:
                time2 = time.strftime('%I:%M %p')
            else:
                time2 = time.strftime('%H:%M')

            day_of_week2 = time.strftime('%A')
            date2 = time.strftime(DATE_FORMAT)

            if time2 != self.time1:
                self.time1 = time2
            if day_of_week2 != self.day_of_week1:
                self.day_of_week1 = day_of_week2
            if date2 != self.date1:
                self.date1 = date2

if __name__ == "__main__":
    time = Clock()
    print("%s, %s / %s" % (time.day_of_week1, time.date1, time.time1))
