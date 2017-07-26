#!/usr/bin/env python
"""
SmartMirror.py
A python program to output data for use with a smartmirror.
It fetches weather, news, and time information.
"""

from traceback import print_exc
from json import loads
import tkinter
from requests import get
from feedparser import parse

### Darksky API weather constants ###
# replace with secret key provided at https://darksky.net/dev/account/
WEATHER_API_TOKEN = '443a029b56964c639cb8f6da87415c20'
WEATHER_LANG = 'en'
WEATHER_UNIT = 'uk2'


class Weather():
    """
    Weather class
    This class contains methods that fetch weather information.
    Weather information is based upon location.
    Location is determined using the device's IP address.
    """


    def __init__(self):
        """
        Weather constructor.
        Stores weather information.
        """

        self.temperature = ''
        self.forecast = ''
        self.location = ''
        self.latitude = ''
        self.longitude = ''
        self.currently = ''
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
                (str(int(weather_obj['currently']['temperature'])), degree_sign)
            # get current weather summary and store in tmp variable
            currently_tmp = weather_obj['currently']['summary']
            # get the forecast summary and store it in tmp variable
            forecast_tmp = weather_obj['hourly']['summary']

            # update weather information
            if self.currently != currently_tmp:
                self.currently = currently_tmp
            if self.forecast != forecast_tmp:
                self.forecast = forecast_tmp
            if self.temperature != temperature_tmp:
                self.temperature = temperature_tmp

        except Exception as exc:
            print_exc()
            print("Error %s. Cannot get weather." % exc)


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

def get_news():
    """
    get_news class
    fetches XML data from the BBC using feedparser
    """

    try:
        # store news headlines in variable
        headlines = []

        ### Fetch XML data from news website ###
        # store XML url in variable
        news_url = "http://feeds.bbci.co.uk/news/uk/rss.xml"
        # parse XML data into Python object and store in variable
        feed = parse(news_url)

        # iterate through XML and store first 5 headlines in self.headlines
        index = 0
        for item in feed.entries[0:5]:
            headlines.insert(index, item.title)
            index += 1

        # return headline info
        return headlines

    except Exception as exc:
        print_exc()
        print("Error %s. Cannot get weather." % exc)

def test_output():
    """
    test_output
    tests output of classes and methods in the program.
    """

    weather = Weather()
    print("The current temperature is %sC" % weather.temperature)
    print("The current summary is: %s" % weather.currently)
    print("The current forecast is: %s" % weather.forecast)
    print("The current location is: %s" % weather.location)

    headlines = get_news()
    for i in range(0, len(headlines)):
        print("Headline %s: %s" % (i+1, headlines[i]))

if __name__ == "__main__":
    test_output()
