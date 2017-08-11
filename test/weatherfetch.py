#!/usr/bin/env python
import requests
import json
import traceback

# variables to use with the Darksky API
weather_api_token = '443a029b56964c639cb8f6da87415c20'
weather_lang = 'en'
weather_unit = 'uk2'

# Class containing methods that fetch weather data based upon your location according to your IP address.
class Weather():
    def __init__(self):
        self.temperature = ''
        self.forecast = ''
        self.location = ''
        self.currently = ''
        self.GetWeather()

    def GetIP(self):
        try:
            ip_url = "https://api.ipify.org?format=json"
            r = requests.get(ip_url)
            ip_json = json.loads(r.text)
            return ip_json['ip']
        except Exception as e:
            traceback.print_exc()
            return "Error: %s. Cannot get ip." % e

    def GetWeather(self):
        try:
            # fetch location information using freegeoip API
            location_req_url = "http://freegeoip.net/json/%s" % self.GetIP()
            r = requests.get(location_req_url)
            location_json = json.loads(r.text)

            latitude = location_json['latitude']
            longitude = location_json['longitude']

            location_tmp = "%s, %s" % (location_json['city'], location_json['region_code'])

            # get weather information
            weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (weather_api_token, latitude, longitude, weather_lang, weather_unit)

            r = requests.get(weather_req_url)
            weather_json = json.loads(r.text)

            # assign weather information to variables
            degree_sign = u'\N{DEGREE SIGN}'
            temperature_tmp = "%s%s" % (str(int(weather_json['currently']['temperature'])), degree_sign) # get current temperature and store in temporary variable
            currently_tmp = weather_json['currently']['summary'] # get current weather summary and store in a temporary variable
            forecast_tmp = weather_json['hourly']['summary'] # get the forecast summary for the next day and store in a temp variable

            # update weather information
            if self.currently != currently_tmp:
                self.currently = currently_tmp
            if self.forecast != forecast_tmp:
                self.forecast = forecast_tmp
            if self.temperature != temperature_tmp:
                self.temperature = temperature_tmp

            if self.location != location_tmp:
                self.location = location_tmp

        except Exception as e:
            traceback.print_exc()
            print ("Error %s. Cannot get weather.") % e

# temporary to for testing the Weather class.
w = Weather()
print("The current temperature is %sC" % w.temperature)
print("The current summary is: %s" % w.currently)
print("The current forecast is: %s" % w.forecast)
print("The current location is: %s" % w.location)
