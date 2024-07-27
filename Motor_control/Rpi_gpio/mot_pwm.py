import Rpi.GPIO as GPIO
from time import sleep

ain1 = 11
ain2 = 12
pwm = 7
stby = 13


GPIO.setmode(GPIO.BCM)


# set up GPIO pins
GPIO.setup(pwm, GPIO.OUT) # Connected to PWMA
GPIO.setup(ain1, GPIO.OUT) # Connected to AIN2
GPIO.setup(ain2, GPIO.OUT) # Connected to AIN1
GPIO.setup(stby, GPIO.OUT) # Connected to STBY



