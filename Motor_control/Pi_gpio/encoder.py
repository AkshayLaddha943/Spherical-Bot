#!/usr/bin/env python

''' 
pigpio examples callback function, for more check here
http://abyz.me.uk/rpi/pigpio/python.html#callback
https://github.com/joan2937/pigpio/blob/master/EXAMPLES/Python/ROTARY_ENCODER/rotary_encoder.py

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

Base calculations

Number of pulses in 1 sec = 1216
Count = 3PPR
Gear ratio = 1:50

Output RPM = ((Pulses Recieved in 1 sec * 60) / PPR) / Gear Ratio

Project - Small spherical bot
Vaibhav Kadam
29 Aug 2019
'''

import pigpio
import time
import rotary_encoder


pos = 0
def callback(way):
    global pos
    pos += way
    print("pos={}".format(pos))

pi = pigpio.pi()
decoder = rotary_encoder.decoder(pi, 24, 25, callback)
time.sleep(300)
decoder.cancel()
pi.stop()