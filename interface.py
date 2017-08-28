#!/usr/bin/env python
"""
SmartMirror.py
A python program to output data for use with a smartmirror.
It fetches weather, news, and time information.
"""

from traceback import print_exc
from json import loads
from time import strftime
from threading import Lock
import locale

from contextlib import contextmanager
from requests import get
from feedparser import parse
from PIL import Image, ImageTk

# try/except to use correct Tkinter library depending on device.
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

### Darksky API weather constants ###
# replace with secret key provided at https://darksky.net/dev/account/
WEATHER_API_TOKEN = '[TOKEN]'
# For full list of language and unit paramaeters see:
# https://darksky.net/dev/docs/forecast
WEATHER_LANG = 'en'
WEATHER_UNIT = 'uk2'
# maps
ICON_LOOKUP = {
    'clear-day': "icons/sun.png",  # Clear Sky
    'wind': "icons/wind.png",  # Wind
    'cloudy': "icons/cloud.png",  # Cloudy day
    'partly-cloudy-day': "icons/sun-cloud.png",  # Partial clouds
    'rain': "icons/rain.png",  # Rain
    'snow': "icons/snow.png",  # Snow
    'snow-thin': "icons/snow.png",  # Sleet
    'fog': "icons/fog.png",  # Fog
    'clear-night': "icons/moon.png",  # Clear night
    'partly-cloudy-night': "icons/moon-cloud.png",  # Partial clouds night
    'thunderstorm': "icons/lightning.png",  # Storm
    'tornado': "icons/tornado.png",  # tornado
    'hail': "icons/hail.png"  # hail
}
### Locale and time constants ###
LOCALE_LOCK = Lock()
# set to your own locale. Use locale -a to list installed locales
UI_LOCALE = ''
# leave blank for 24h time format
TIME_FORMAT = None
# check python doc for strftime() for more date formatting options
DATE_FORMAT = "%b %d, %Y"

### Tkinter formatting constants ###
XL_TEXT = 94
LG_TEXT = 48
MD_TEXT = 28
SM_TEXT = 18


@contextmanager
def setlocale(name):
    """
    setlocale class
    used to set the locale using system locale for accurate time information.
    """

    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)


class Weather(tk.Frame):
    """
    Weather class
    This class contains methods that fetch weather information.
    Weather information is based upon location.
    Location is determined using the device's IP address.
    """


    def __init__(self, parent):
        """
        Weather constructor.
        Stores weather information.
        """

        tk.Frame.__init__(self, parent, bg='black')
        # data storage variables
        self.temperature = ''
        self.forecast = ''
        self.location = ''
        self.latitude = ''
        self.longitude = ''
        self.currently = ''
        self.icon = ''

        # tkinter settings
        self.degree_frame = tk.Frame(self, bg="black")
        self.degree_frame.pack(side=tk.TOP, anchor=tk.W)

        self.temperature_label = tk.Label(self.degree_frame, \
                                          font=('Lato', XL_TEXT), \
                                          fg='white', bg="black")
        self.temperature_label.pack(side=tk.LEFT, anchor=tk.N)

        self.icon_label = tk.Label(self.degree_frame, bg="black")
        self.icon_label.pack(side=tk.LEFT, anchor=tk.N, padx=20, pady=25)

        self.currently_label = tk.Label(self, font=('Lato', MD_TEXT), \
                                        fg="white", bg="black")
        self.currently_label.pack(side=tk.TOP, anchor=tk.W)

        self.forecast_label = tk.Label(self, font=('Lato', SM_TEXT), \
                                       fg='white', bg='black')
        self.forecast_label.pack(side=tk.TOP, anchor=tk.W)

        self.location_label = tk.Label(self, font=('Lato', SM_TEXT), \
                                       fg="white", bg="black")
        self.location_label.pack(side=tk.TOP, anchor=tk.W)

        self.get_location()
        self.get_weather()

    def get_location(self):
        """
        get_location
        Method to fetch device location based upon IP address.
        """

        try:
            ### Fetch location using freegeoip API ###
            # store location URL. Uses IP fetched by get_ip() in variable
            location_req_url = "http://freegeoip.net/json/%s" % self.get_ip()
            # fetch data from URL in location_req_url and store in variable
            req = get(location_req_url)
            # convert fetched data to python object and store in variable
            location_obj = loads(req.text)

            # change latitude variable if device has moved.
            if self.latitude != location_obj['latitude']:
                self.latitude = location_obj['latitude']
                # change latitude variable if device has moved.
                if self.longitude != location_obj['longitude']:
                    self.longitude = location_obj['longitude']

            # get current location and store in tmp variable
            location_tmp = "%s, %s" % \
                    (location_obj['city'], location_obj['region_code'])

            # update weather information
            if self.location != location_tmp:
                self.location = location_tmp
                self.location_label.config(text=location_tmp)

        except Exception as exc:
            print_exc()
            return "Error: %s. Cannot get location." % exc

    def get_weather(self):
        """
        get_weather
        Method that fetches weather information
        """

        try:
            ### Get weather information using Darksky API ###
            # store the darksky API URL in variable
            weather_req_url =\
                "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" \
                % (WEATHER_API_TOKEN, self.latitude, self.longitude,\
                   WEATHER_LANG, WEATHER_UNIT)
            # fetch data from URL in weather_req_url and store in a variable
            req = get(weather_req_url)
            # convert fetched data to puthon object and store in variable
            weather_obj = loads(req.text)

            ### Assign weather information to variables ###
            # store unicode degree character in variable
            degree_sign = u'\N{DEGREE SIGN}'
            # get current temperature and store in tmp variable
            temperature_tmp = "%s%s" % \
                    (str(int(weather_obj['currently']['temperature'])), \
                     degree_sign)
            # get current weather summary and store in tmp variable
            currently_tmp = weather_obj['currently']['summary']
            # get the forecast summary and store it in tmp variable
            forecast_tmp = weather_obj['hourly']['summary']
            # get the ID of the icon and store in variable
            icon_id = weather_obj['currently']['icon']
            icon_tmp = None

            # fetch weather icon informaton stored in weather_obj
            if icon_id in ICON_LOOKUP:
                icon_tmp = ICON_LOOKUP[icon_id]

            if icon_tmp is not None:
                if self.icon != icon_tmp:
                    # set self.icon to the new icon
                    self.icon = icon_tmp
                    # open the image file
                    image = Image.open(icon_tmp)
                    # resize the image and antialias
                    image = image.resize((100, 100), Image.ANTIALIAS)
                    image = image.convert('RGB')
                    # convert image to tkinter object and store in variable
                    photo = ImageTk.PhotoImage(image)

                    # apply settings to self.icon_label
                    self.icon_label.config(image=photo)
                    self.icon_label.image = photo
            else:
                # remove image
                self.icon_label.config(image='')

            # update weather information
            if self.currently != currently_tmp:
                self.currently = currently_tmp
                self.currently_label.config(text=currently_tmp)
            if self.forecast != forecast_tmp:
                self.forecast = forecast_tmp
                self.forecast_label.config(text=forecast_tmp)
            if self.temperature != temperature_tmp:
                self.temperature = temperature_tmp
                self.temperature_label.config(text=temperature_tmp)

        except Exception as exc:
            print_exc()
            print("Error %s. Cannot get weather." % exc)

        self.after(300000, self.get_weather)


    @staticmethod
    def get_ip():
        """
        get_ip
        gets the IP address of the device and returns it
        """

        try:
            ### Fetch IP address using IPify API ###
            # store ipify API URL in variable
            ip_url = "https://api.ipify.org?format=json"
            # fetch data from URL in ip_url and store in variable
            req = get(ip_url)
            # convert fetched data to python object and store in variable
            ip_obj = loads(req.text)

            # return value stored in 'ip' JSON attribute
            return ip_obj['ip']

        except Exception as exc:
            print_exc()
            return "Error: %s. Cannot get IP." % exc


class Clock(tk.Frame):
    """
    Clock class
    Outputs date and time info to tkinter GUI.
    """
    def __init__(self, parent):
        """
        Clock constructor
        Stores time information and tkinter configuration options.
        """

        self.time = ''
        self.day = ''
        self.date = ''

        tk.Frame.__init__(self, parent, bg='black')
        self.time_label = tk.Label(self, font=('Lato', LG_TEXT),\
                                   fg="white", bg="black")
        self.time_label.pack(side=tk.TOP, anchor=tk.E, fill=tk.X)

        self.date_label = tk.Label(self, font=('Lato', SM_TEXT),\
                                   fg="white", bg="black")
        self.date_label.pack(side=tk.TOP, anchor=tk.E)

        self.day_label = tk.Label(self, font=('Lato', SM_TEXT),\
                                  fg="white", bg="black")
        self.day_label.pack(side=tk.TOP, anchor=tk.E)
        self.update_time()

    def update_time(self):
        """
        update_time method
        updates the time using system locale.
        """

        with setlocale(UI_LOCALE):
            if TIME_FORMAT == 12:
                time_tmp = strftime('%I:%M %p')
            else:
                time_tmp = strftime('%H:%M')

            day_tmp = strftime('%A')
            date_tmp = strftime(DATE_FORMAT)

            if time_tmp != self.time:
                self.time = time_tmp
                self.time_label.config(text=time_tmp)
            if date_tmp != self.date:
                self.date = date_tmp
                self.date_label.config(text=date_tmp)
            if day_tmp != self.day:
                self.day = day_tmp
                self.day_label.config(text=day_tmp)

            self.time_label.after(200, self.update_time)


class News(tk.Frame):
    """
    News class
    Fetches news from BBC RSS feed and outputs top 5 headlines.
    """


    def __init__(self, parent):
        """
        News contructor
        stores headline data for News object
        """

        tk.Frame.__init__(self, parent)
        self.config(bg='black')
        self.title = 'News'
        self.news_label = tk.Label(self, text=self.title, \
                                   font=('Lato', MD_TEXT), \
                                   fg='white', bg='black')
        self.news_label.pack(side=tk.TOP, anchor=tk.E)
        self.headlines_label = tk.Label(self, font=('Lato', SM_TEXT), \
                              fg='white', bg='black')
        self.headlines_label.pack(side=tk.TOP, anchor=tk.N)

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

            # join the contents of headlines into
            headlines_tmp = '\n'.join(headlines)
            self.headlines_label.config(text=headlines_tmp)

        except Exception as exc:
            print_exc()
            print("Error %s. Cannot get news." % exc)

        self.after(300000, self.get_news)

class BuildGUI:
    """
    BuildGUI class
    draws the GUI and contains methods for toggling fullcreen
    """


    def __init__(self):
        """
        BuildGUI constructor
        sets the configuration options for the GUI and builds it.
        """

        self.root = tk.Tk()
        self.root.config(background='black')
        self.left_frame = tk.Frame(self.root, background='black')
        self.right_frame = tk.Frame(self.root, background='black')
        self.bottom_frame = tk.Frame(self.root, background='black')
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.YES)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=tk.YES)
        self.state = False

        # Return toggles between fullscreen modes. Escape exits fullscreen
        self.root.bind("<Return>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.end_fullscreen)

        # clock
        self.clock = Clock(self.right_frame)
        self.clock.pack(side=tk.RIGHT, anchor=tk.N, padx=50, pady=50)
        #weather
        self.weather = Weather(self.left_frame)
        self.weather.pack(side=tk.LEFT, anchor=tk.N, padx=50, pady=50)
        #news
        self.news = News(self.bottom_frame)
        self.news.pack(side=tk.RIGHT, anchor=tk.S, padx=50, pady=50)
        self.news.headlines_label.config(justify=tk.RIGHT)

    def toggle_fullscreen(self, event=None):
        """
        toggle_fullscreen method
        toggles the GUI's fullscreen state when user presses return
        """

        self.state = not self.state
        self.root.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        """
        end_fullscreen method
        ends the GUI's fullscreen state when user presses escape.
        """
        self.state = False
        self.root.attributes("-fullscreen", False)
        return "break"


# Start the program.
if __name__ == "__main__":
    WINDOW = BuildGUI()
    WINDOW.root.mainloop()
