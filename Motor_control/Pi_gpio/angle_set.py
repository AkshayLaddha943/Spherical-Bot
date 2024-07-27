#!/usr/bin/env python

import time
import pigpio

"""
Code description
================

Python code written for closed-loop position control of DC motors using encoder based feedback.

Author: Kaustubh Sadekar

Motor specifications used for experiment
========================================

Motor model = GA12 N20 | 50 RPM 6V motor
Gear ratio = 1:298

"""

"""
NOTES :
"""



pins_dict = {"m1a":17, "m1b":18, "p1":13, "ch2":24, "ch1":25}

class N20_Motor:

	def __init__(self,pins_dict):
		self.m1a = pins_dict["m1a"]
		self.m1b = pins_dict["m1b"]
		self.p1 = pins_dict["p1"]
		self.chPin1 = pins_dict["ch1"]
		self.chPin2 = pins_dict["ch2"]
		self.ch1_state = 0
		self.ch2_state = 0
		self.clockwise_rot = None
		self.ticks = 0
		self.TPR = 445	 #6*330 #445 # Ticks per revolution after experimentation 
		self.theta = 0
		self.temp_da = None # Temporary value of duty cycle at channel A of motor
		self.temp_db = None
		self.derivator = 0 
		self.integrator = 0
		self.i_min = -10
		self.i_max = 10

		self.pi = pigpio.pi()

		self.pi.set_mode(self.m1a,pigpio.OUTPUT)
		self.pi.set_mode(self.m1b,pigpio.OUTPUT)
		self.pi.set_mode(self.p1,pigpio.OUTPUT)  #PWMA 13         7

		self.pi.set_PWM_frequency(self.m1a,10000)
		self.pi.set_PWM_range(self.m1a,100)

		self.pi.set_PWM_frequency(self.m1b,10000)
		self.pi.set_PWM_range(self.m1b,100)

		self.pi.set_mode(self.chPin1,pigpio.INPUT)
		self.pi.set_pull_up_down(self.chPin1, pigpio.PUD_UP)
		self.ch1 = self.pi.callback(self.chPin1,pigpio.EITHER_EDGE, self.callbackFn)
		
		self.pi.set_mode(self.chPin2,pigpio.INPUT)
		self.pi.set_pull_up_down(self.chPin2, pigpio.PUD_UP)
		self.ch2 = self.pi.callback(self.chPin2,pigpio.EITHER_EDGE, self.callbackFn)
		

	def clockwise(self,speed):
		speed = max(speed,40)
		speed = min(speed,100)
		self.pi.write(27,1)
		self.pi.write(self.m1a,0)
		self.pi.write(self.m1b,1)
		self.pi.set_PWM_dutycycle(self.p1,abs(speed))
		

	def anti_clockwise(self,speed):
		speed = max(speed,40)
		speed = min(speed,100)
		self.pi.write(27,1)
		self.pi.write(self.m1a,1)
		self.pi.write(self.m1b,0)
		self.pi.set_PWM_dutycycle(self.p1,abs(speed))
		
	def pause_motors(self):
		self.pi.set_PWM_dutycycle(self.p1,1)
		self.pi.write(27,0)

	def resume_motors(self):
		self.pi.set_PWM_dutycycle(self.p1,int(self.temp_da))


	def clean_all(self):
		self.pi.write(self.m1a,0)
		self.pi.write(self.m1b,0)
		self.pi.stop()

	def callbackFn(self, gpio, level, tick):
		if gpio == self.chPin1:
			self.ch1_state = level
			if self.ch1_state:  # Only in case of rising edge on ch1
				if self.ch2_state:
					self.clockwise_rot = True
					self.ticks+=1
				else:
					self.clockwise_rot = False
					self.ticks-=1

				self.theta = (self.ticks//self.TPR+(self.ticks%self.TPR)*1.0/self.TPR)*360
				#print(self.theta)

		else:
			self.ch2_state = level

	def motion1(self,speed=100):
		self.clockwise(speed=50)
		counter = 0
		while True:
			print(self.theta)
			if self.theta > 360:
				self.anti_clockwise(speed=50)
			if self.theta < 0:
				self.clockwise(speed=50)

	def set_motor_angle(self,theta,mode=0):
		Kp = 1	
		ki = 0.05
		kd = 0.1
		prev_err = 0
		if mode == 0:
			while True:
				err = theta - self.theta

				if abs(err) < 0.5:
					self.pause_motors()
					break

				P = Kp*err

				self.derivator = err - prev_err
				D = kd*self.derivator
				prev_err = err

				self.integrator = self.integrator + err
				I = self.integrator*ki

				duty = int(P + I + D)
				
				print duty,self.theta
				
				if duty < 0:
					self.anti_clockwise(speed=duty)
					print("In anti clockwise")
				if duty > 0:
					print("In clockwise")
					self.clockwise(speed=duty)
				


if __name__ == '__main__':

    motor = N20_Motor(pins_dict)
    try :
    	while True:
    	
	        angle = int(input("Set the angle : "))
	        #motor.callbackFn
	        motor.set_motor_angle(angle)
    except KeyboardInterrupt:
    	motor.clean_all()
