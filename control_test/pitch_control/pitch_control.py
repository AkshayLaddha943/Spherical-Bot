import time
import pigpio
import socket
import sys
import board
import busio
import adafruit_bno055
import math
import datetime
import csv
import keyboard

# Use these lines for I2C IMU feedback
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)

# Setting up PWM for servo
pi = pigpio.pi()
pi.set_mode(22, pigpio.OUTPUT)
pi.set_mode(23, pigpio.OUTPUT)

pitch_data = []
# Setting up the N20 motor
pi.set_mode(13, pigpio.OUTPUT)  # PWMA 13
pi.set_mode(17, pigpio.OUTPUT)  # AIN2 17
pi.set_mode(18, pigpio.OUTPUT)  # AIN1 18
pi.set_mode(27, pigpio.OUTPUT)  # STBY 27

global pitch_actual
global Kp_pitch

def map(value, axes_min, axes_max, actuate_min, actuate_max):
    axes_span = axes_max - axes_min
    actuate_span = actuate_max - actuate_min
    value_scaled = (float(value - axes_min) / float(axes_span))
    return int(actuate_min + (value_scaled * actuate_span))

def front_servo(angle):
    # Angle here is negated because it's in the opposite direction facing
    pulse_width = map(-angle, -30, 30, 1300, 2000)
    pi.set_servo_pulsewidth(22, pulse_width)

def rear_servo(angle):
    pulse_width = map(angle, -30, 30, 1000, 1800)
    pi.set_servo_pulsewidth(23, pulse_width)

def get_pitch():
    yaw, roll, pitch = sensor.euler
    print('Im getting pitch ', pitch)
    return pitch

def forward_ascent():
    for pwm_a in range(mot_pwm, 0, -5):
        motor(True, pwm_a)
        time.sleep(0.05)

def backward_descent():
    for pwm_b in range(mot_pwm, 0, -5):
        motor(False, pwm_b)
        time.sleep(0.05)

def write_to_csv(data, filename):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def motor(mot_dir, mot_pwm):
    if mot_dir == True:
        pi.write(27, 1)  # disable standby active low
        pi.write(18, 0)
        pi.write(17, 1)
        pi.set_PWM_dutycycle(13, mot_pwm)
    elif mot_dir == False:
        pi.write(27, 1)  # disable standby active low
        pi.write(18, 1)
        pi.write(17, 0)
        pi.set_PWM_dutycycle(13, mot_pwm)
    else:
        pi.write(18, 0)
        pi.write(17, 0)
        pi.set_PWM_dutycycle(13, 0)
        pi.write(27, 0)

with open('output.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['roll', 'pitch', 'yaw', 'time'])  # Write header

# Setting up Servo for Android control
'''
HOST = ''
PORT = 6000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created.")
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error code: ' + str(msg))
    sys.exit()
print('Socket bind complete')
s.listen(10)
print('Socket now listening')
conn, addr = s.accept()

flag_run = False
'''

Kp_pitch = 0.00876
set_pt_pitch = 0.0

try: 
    while True:
        '''
        data = conn.recv(1024)

        if not data:
            break
        
        pos_b = data.rfind(b'b')
        data = data[:pos_b]
        pos_a = data.rfind(b'a')
        data = data[pos_a + 1:]
        pos_y = bytes.find(data, b'y')
        pos_p = data.rfind(b'p')

        str_x = data[1:pos_y]
        str_y = data[pos_y + 1:pos_p]
        str_p = data[pos_p + 1:]
        
        x = int(str_x) - 50
        y = int(str_y) - 50
        p = int(str_p) - 10
        '''
        
        p = 50
        servo_angle = map(p, 20, 80, -30, 30)
        front_servo(servo_angle)
        rear_servo(servo_angle)
        
        pitch_actual = get_pitch()
        timestamp = datetime.datetime.now()
        pitch_data.append((pitch_actual, timestamp))
        
        for row in pitch_data:
            write_to_csv(row, 'output.csv')
        
        pitch_err = set_pt_pitch - pitch_actual
        user_pwm = 185  # map(y, 0, 65, 0, 200)
        mot_pwm = max(0, min(200, 140 * Kp_pitch * pitch_err + user_pwm))
        mot_dir = True
        motor(mot_dir, mot_pwm)
        flag_run = True

        if keyboard.is_pressed('s'):
            print("ight imma head out")
            break

    print('Socket is now closing')
    # conn.close()
    pi.stop()

except KeyboardInterrupt:
    print('Socket is now closing')
    #conn.close()
    pi.stop()
