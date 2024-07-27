import time
import pigpio
import math
import pygame


# Setting up PWM for servo
pi = pigpio.pi()
pi.set_mode(22, pigpio.OUTPUT)
pi.set_mode(23, pigpio.OUTPUT)

# Setting up the N20 motor
pi.set_mode(13, pigpio.OUTPUT)  # PWMA 13
pi.set_mode(17, pigpio.OUTPUT)  # AIN2 17
pi.set_mode(18, pigpio.OUTPUT)  # AIN1 18
pi.set_mode(27, pigpio.OUTPUT)  # STBY 27

global roll_actual

# Initialize pygame
pygame.init()
pygame.display.init()
screen = pygame.display.set_mode((100, 100))
pygame.display.set_caption("Keyboard Control")

def map(value, axes_min, axes_max, actuate_min, actuate_max):
    axes_span = axes_max - axes_min
    actuate_span = actuate_max - actuate_min
    value_scaled = (float(value - axes_min) / float(axes_span))
    return int(actuate_min + (value_scaled * actuate_span))

def front_servo(angle):
    pulse_width = map(-angle, -30, 30, 1300, 2000)
    pi.set_servo_pulsewidth(22, pulse_width)

def rear_servo(angle):
    pulse_width = map(angle, -30, 30, 1000, 1800)
    pi.set_servo_pulsewidth(23, pulse_width)

def get_roll():
    yaw, roll, pitch = sensor.euler
    return roll

def roll_control():
    Kp = 1
    P = Kp * roll_err
    front_servo(P)
    rear_servo(P)
    print('I\'m in roll controller P ', P)

def forward_ascent():
    for pwm_a in range(mot_pwm, 0, -5):
        motor(True, pwm_a)
        time.sleep(0.05)

def backward_descent():
    for pwm_b in range(mot_pwm, 0, -5):
        motor(False, pwm_b)
        time.sleep(0.05)

def motor(mot_dir, mot_pwm):
    if mot_dir:
        pi.write(27, 1)  # disable standby active low
        pi.write(18, 0)
        pi.write(17, 1)
        pi.set_PWM_dutycycle(13, mot_pwm)
    else:
        pi.write(27, 1)  # disable standby active low
        pi.write(18, 1)
        pi.write(17, 0)
        pi.set_PWM_dutycycle(13, mot_pwm)

mot_dir = True
mot_pwm = 0
flag_run = False

running = True
servo_angle = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                mot_pwm = map(50, 0, 100, 0, 200)  # Adjust this mapping as needed
                mot_dir = True
                motor(mot_dir, mot_pwm)
                flag_run = True
            elif event.key == pygame.K_s:
                mot_pwm = map(50, 0, 100, 0, 200)  # Adjust this mapping as needed
                mot_dir = False
                motor(mot_dir, mot_pwm)
                flag_run = True
            elif event.key == pygame.K_a:
                servo_angle = map(20, 20, 80, -30, 30)  # Adjust this mapping as needed
                front_servo(servo_angle)
                rear_servo(servo_angle)
            elif event.key == pygame.K_d:
                servo_angle = map(80, 20, 80, -30, 30)  # Adjust this mapping as needed
                front_servo(servo_angle)
                rear_servo(servo_angle)
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_w, pygame.K_s]:
                motor(mot_dir, 0)
                flag_run = False
            elif event.key in [pygame.K_a, pygame.K_d]:
                front_servo(0)
                rear_servo(0)

    roll_actual = get_roll()
    set_pt_roll = 0.0
    roll_err = (set_pt_roll - roll_actual)
    roll_control()

print('Socket is now closing')
pi.stop()
pygame.quit()

