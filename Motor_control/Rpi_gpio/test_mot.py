#!/usr/bin/env python


import time
import RPi.GPIO as GPIO

# Declare the GPIO settings
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
# set up GPIO pins
GPIO.setup(7, GPIO.OUT) # Connected to PWMA
GPIO.setup(11, GPIO.OUT) # Connected to AIN2
GPIO.setup(12, GPIO.OUT) # Connected to AIN1
GPIO.setup(13, GPIO.OUT) # Connected to STBY


# Disable STBY (standby)
GPIO.output(13, GPIO.HIGH)
p=GPIO.PWM(7,1000)
#p.start(25)

print "Moving Clockwise"
# Drive the motor clockwise
GPIO.output(12, GPIO.LOW) # Set AIN1
GPIO.output(11, GPIO.HIGH) # Set AIN2
GPIO.output(7, GPIO.HIGH)
time.sleep(5)



print "Moving Anit-Clockwise"
GPIO.output(7, GPIO.HIGH)
GPIO.output(12, GPIO.HIGH) # Set AIN1
GPIO.output(11, GPIO.LOW) # Set AIN2

time.sleep(10)


# Reset all the GPIO pins by setting them to LOW
GPIO.output(12, GPIO.LOW) # Set AIN1
GPIO.output(11, GPIO.LOW) # Set AIN2
GPIO.output(7, GPIO.LOW) # Set PWMA
GPIO.output(13, GPIO.LOW) # Set STBY

GPIO.cleanup()