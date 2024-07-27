#!/usr/bin/env python

'''
Servo control sg90 
Pinout GPIO 22 for PWM, with pigpio any gpio can be made to generate pwm
set_servo_pulsewidth(GPIO number, pulse_width in ms)

Following values are in msw
1500 - center
2000 - safe clockwise
800 -  safe anti clockwise
0 - stop

Pin out 
GPIO 22 Servo 1
GPIO 23 Servo 2

Project - Small spherical bot
Vaibhav Kadam
28 Aug 2019
'''

import pigpio
import time

pi =  pigpio.pi()                    # object to access class pigpio
pi.set_mode(22, pigpio.OUTPUT)
pi.set_mode(23, pigpio.OUTPUT)
i= 0
while(i<=1):

    pi.set_servo_pulsewidth(22, 1600)  # set_servo_pulsewidth(pin_no, pulse_width in ms)
    pi.set_servo_pulsewidth(23, 1500)
    time.sleep(2)

    pi.set_servo_pulsewidth(22, 1500) # set_servo_pulsewidth(pin_no, pulse_width in ms)
    pi.set_servo_pulsewidth(23, 1600)
    time.sleep(2)

    i = i+1

  

pi.stop()

#pin 22 1600 calibrated value
#pin 23 1400 calibrated value
