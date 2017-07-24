#!/usr/bin/env python
"""
SmartMirror.py
A python program to output data for use with a smartmirror.
It fetches weather, news, and time information.

"""
from traceback import print_exec
from json import loads
import tkinter
from requests import get
from feedparser import parse

# Darksky API weather constants
WEATHER_API_TOKEN = '443a029b56964c639cb8f6da87415c20'
WEATHER_LANG = 'en'
WEATHER_UNIT = 'uk2'


class Weather():
    """
    Weather class
    This class contains methods that fetch weather information.
    Weather information is based upon location.
    Location is determined by IP address.
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
        self.get_weather()

    def get_ip(self):
        """
        get_ip
        gets the IP address of the device and returns it
        """

        try:
            ip_url = "https://api.ipify.org?format=json"
            req = get(ip_url)
            ip_json = loads(req.text)
            return ip_json['ip']

        except Exception as e:
            print_exec()
            return "Error: %s. Cannot get IP." % e

        def get_location(self):
            """
            get_location
            Method to fetch device location based upon IP address.
            """

            # Fetch location using freegeoip API
            location_req_url = "http://freegeoip.net/json/%s" % self.get_ip() # variable to store location URL
            req = get(location_req_url) # fetch data from URL in location_req_url and store in variable
            location_obj = loads(req.text) # convert fetched data to python object and store in variable

            if self.latitude != location_obj['latitude']:
                self.latitude = location_obj['latitude']

            if self.longitude != location_obj['longitude']:
                self.longitude = location_obj['longitude']

        def get_weather(self):
            """
            get_weather
            Method that fetches weather information
            """
