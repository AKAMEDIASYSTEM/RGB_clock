import atexit
import urllib2
import math
import datetime
import time
import os
import sys
import threading
import subprocess
import re
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as pwm
from Queue import Queue

interval = 120 # in seconds, it turns out!
greenPin = 'P8_13'
bluePin = 'P9_14'
redPin = 'P8_19'

def exit_handler():
    print 'exiting'
    pwm.stop(greenPin)
    pwm.stop(redPin)
    pwm.stop(bluePin)
    pwm.cleanup()

def mapVals(val, inMin, inMax, outMin, outMax):
    toRet = float(outMin + float(outMax - outMin) * float(float(val - inMin) / float(inMax - inMin)))
    # if (toRet > outMax):
    #     toRet = outMax
    # if (toRet < outMin):
    #     toRet = outMin
    return clamp(toRet, outMin, outMax)

def clamp(val, min, max):
    if (val < min):
        val = min
    if (val > max):
        val = max
    return val

def handleTime():
    t = datetime.datetime.today()
    if t.minute ==0:
        print 'it is the top of the hour!'
        pwm.set_duty_cycle(bluePin, 100)
        pwm.set_duty_cycle(redPin, 0)
        pwm.set_duty_cycle(greenPin,0)
    else:
        r = mapVals(t.minute, 0, 59, 0, 100)
        pwm.set_duty_cycle(redPin, r)
        g = 100-r
        print 'should be %s and %s percent red and green' %(r, g)
        pwm.set_duty_cycle(greenPin, g)
        pwm.set_duty_cycle(bluePin, 0.0)

#PWM.start(channel, duty, freq=2000)
pwm.start(greenPin, 10.0, 2000.0)
pwm.start(redPin, 10.0, 2000.0)
pwm.start(bluePin, 10.0, 2000.0)
atexit.register(exit_handler)

while True:
    handleTime()
    time.sleep(30)