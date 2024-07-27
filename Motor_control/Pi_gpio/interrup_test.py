#!/usr/bin/env python
''' 
pigpio examples callback function, for more check here
http://abyz.me.uk/rpi/pigpio/python.html#callback

***
callback(user_gpio, edge, func)
Calls a user supplied function (a callback) whenever the specified GPIO edge is detected.

Parameters

user_gpio:= 0-31.
     edge:= EITHER_EDGE, RISING_EDGE (default), or FALLING_EDGE.
     func:= user supplied callback function.
***


GPIO 24 -> CHA -> DSO X Yellow 
GPIO 25 -> CHB -> DSO Y Red

Project - Small spherical bot
Vaibhav Kadam
29 Aug 2019
'''
import pigpio
from time import sleep

pi = pigpio.pi()

pi.set_mode(24,pigpio.INPUT)
pi.set_mode(25,pigpio.INPUT)

pi.set_pull_up_down(24, pigpio.PUD_UP)
pi.set_pull_up_down(25, pigpio.PUD_UP)

def callback(gpio, level, tick):
   print(gpio, level, tick)

#def pulse(gpio, level, tick):

ch1 = pi.callback(24,pigpio.EITHER_EDGE, callback)
ch2 = pi.callback(25,pigpio.EITHER_EDGE, callback)

#ch2 = pi.callback(25)
#print(ch2.tally())

sleep(5)


#ch2.reset_tally()

ch1.cancel() # To cancel callback cb1.
ch2.cancel() # To cancel callback cb1.