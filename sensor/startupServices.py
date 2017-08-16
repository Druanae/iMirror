# -*- coding: utf-8 -*-
from gpiozero import DistanceSensor
import os
import commands
from subprocess import call
#from alexa_client import AlexaClient
import time
import webbrowser

#distancesensor setup - distance values are in metres
ultrasonic = DistanceSensor(echo=17, trigger=4, threshold_distance=0.2, max_distance=3)

#starting services - webserver and chromium started in kioskmode before this
#       from autostart



###########################
#waiting for internet connection#alexa voice sample app

webbrowser.open('http://0.0.0.0:5005') #webserver black screen, just to make sure
###########################


#switching logic

def inRange():
    print("in range")
    webbrowser.open('httpp://0.0.0.0:5005/index')
    #play prerecorded alexa audio?

def outOfRange():
    time.sleep(5)
    webrowser.open('http://0.0.0.0:5005')
    #alexa exits apps? maybe impossible with AVS sample app(only this is capable to log you in)
    #alexa_client is capable, but I don't know a way to connect it to a developer account
      

#distanceSensor control    
ultrasonic.when_out_of_range = outOfRange
ultrasonic.when_in_range = inRange









