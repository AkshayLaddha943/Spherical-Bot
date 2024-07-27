# Servo Control
import time
import pigpio
import socket
import sys
import board
import busio
import adafruit_bno055
import datetime
import csv

from scipy.signal import find_peaks
#import matplotlib.pyplot as plt
#import matplotlib.animation as animation

# Use these lines for I2C IMU feedback
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)


#Setting up pwm for servo
pi =  pigpio.pi()                    
pi.set_mode(22, pigpio.OUTPUT)
pi.set_mode(23, pigpio.OUTPUT)

pitch_data=[]
roll_data=[]
yaw_data=[]
timestamp_data=[]
#  Setting up the N20 motor  
#pi.setmode(GPIO_ pin number, IN/OUT)

pi.set_mode(13,pigpio.OUTPUT)  #PWMA 13        7
pi.set_mode(17,pigpio.OUTPUT)  #AIN2 17       11
pi.set_mode(18,pigpio.OUTPUT)  #AIN1 18        12
pi.set_mode(27,pigpio.OUTPUT)  #STBY 27        13

global roll_actual

class PIDController:
    def __init__(self, kp, kd, ki, setpoint):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpt = setpoint
        self.prev_err = 0
        self.integral = 0
    
    def update(self, error, dt):
        derivative = (error-self.prev_err) / dt
        self.integral += error * dt
        pid_output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.prev_err = error
        return pid_output
    

Kp = 2.0
Kd = 0.3
Ki = 1.3

setpnt = 0.0

pidcontrol = PIDController(kp=Kp, ki=Ki, kd=Kd, setpoint=setpnt)
    
    
def map(value, axes_min, axes_max, actuate_min, actuate_max):
    axes_span = axes_max-axes_min
    actuate_span = actuate_max-actuate_min
    value_scaled = (float(value - axes_min)/float(axes_span))
    return int(actuate_min+(value_scaled*actuate_span))


def front_servo(angle):

    #angle here is negated because its in opposite direction facing
    pulse_width = map(-angle, -30, 30, 1300, 2000) 
    pi.set_servo_pulsewidth(22, pulse_width)

def rear_servo(angle):

    pulse_width = map(angle, -30, 30, 1000, 1800)
    pi.set_servo_pulsewidth(23, pulse_width)

def get_pitch():
	yaw, roll, pitch = sensor.euler
	print('Im geting pitch ',pitch)
	return pitch

def get_yaw():
	yaw, roll, pitch = sensor.euler
	print('Im geting yaw ',yaw)
	return yaw

def get_roll():
	yaw, roll, pitch = sensor.euler
	print('Im geting roll ',roll)
	return roll

# def roll_control():
# 	Kp = 1
# 	P = Kp*roll_err
# 	front_servo(P)
# 	rear_servo(P)
# 	print('Im in roll controller P ',P) 

def forward_ascent():
	for pwm_a in range(80,0, -10):
		motor(True, pwm_a)
		time.sleep(0.25)

def backward_descent():
	for pwm_b in range(80,0, -10):
		motor(False, pwm_b)
		time.sleep(0.25)

def motor(mot_dir, mot_pwm):

    if(mot_dir == True ) :
        pi.write(27,1)        #disable standby active low
        pi.write(18,0)
        pi.write(17,1)
        pi.set_PWM_dutycycle(13,mot_pwm)


    elif(mot_dir == False) :
        pi.write(27,1)        #disable standby active low
        pi.write(18,1)
        pi.write(17,0)
        pi.set_PWM_dutycycle(13,mot_pwm)

    else:
        pi.write(18,0)
        pi.write(17,0)
        pi.set_PWM_dutycycle(13, 0)
        pi.write(27,0)

#fig, ax = plt.subplots()
#line, = ax.plot([], [], 'r-', label='Roll')
#setpoint_line, = ax.plot([], [], 'b--', label='Setpoint')
#ax.set_ylim(-40, 40)
#ax.set_xlim(0, 100)
#ax.set_xlabel('Time')
#ax.set_ylabel('Roll')
#ax.legend()
#ax.grid()

#def init():
 #   line.set_data([], [])
 #   setpoint_line.set_data([], [])
 #   return line, setpoint_line

#def update_plot():
#    roll_actual = get_roll()
#    error = setpnt - roll_actual
#    dt = 0.1  # Adjust time step as needed
#    ctrl_signal = pidcontrol.update(error=error, dt=dt)
#    front_servo(ctrl_signal)
#    rear_servo(ctrl_signal)

#    roll_data.append(roll_actual)
#    timestamp_data.append(len(roll_data) * dt)  # Using the length of roll_data to approximate time
#    line.set_data(timestamp_data, roll_data)
#    setpoint_line.set_data(timestamp_data, [setpnt]*len(timestamp_data))

#    return line, setpoint_line

#ani = animation.FuncAnimation(fig, update_plot, init_func=init, blit=True, interval=100)

#plt.show()

def write_to_csv(data, filename):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

with open('output.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['roll', 'pitch', 'yaw', 'time'])  # Write header
    for row in pitch_data:
        writer.writerow(row)

def calculate_oscillation_period(roll_data, timestamp_data):
    peaks, _ = find_peaks(roll_data)
    if len(peaks) > 1:
        periods = [(timestamp_data[peaks[i]] - timestamp_data[peaks[i-1]]).total_seconds() for i in range(1, len(peaks))]
        Pu = sum(periods) / len(periods) if periods else 0
        return Pu
    return None

#Setting up Servo for Android control
'''HOST = ''
PORT = 6000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("socket created.")
try:
        s.bind((HOST,PORT))
except socket.error as msg:
        print ('Bind failed. Error code: ' + str(msg))
        sys.exit()
print ('Socket bind complete')
s.listen(10)
print ('socket now listening')
conn, addr = s.accept()

flag_run = False

'''
try:
    while True:
        x=0
        y=6.5
        dt = 0.25
        
        mot_pwm = map(y,-65,65, 20, 110)
        mot_dir = True
        print("Forward")
        motor(mot_dir, mot_pwm)
        flag_run = True
        
        roll_actual = get_roll()
        error = setpnt - roll_actual    
        ctrl_signal = pidcontrol.update(error=error, dt=dt)
        front_servo(ctrl_signal)
        rear_servo(ctrl_signal)
        
        pitch_actual= get_pitch()
        yaw_actual= get_yaw()
        roll_data.append(roll_actual)
        timestamp = datetime.datetime.now() 
        timestamp_data.append(timestamp)
        pitch_data.append([roll_actual,pitch_actual,yaw_actual, timestamp])

        if len(roll_data) > 20:  # Analyze data after collecting enough points
            Pu = calculate_oscillation_period(roll_data, timestamp_data)
            if Pu:
                print(f"Current Oscillation Period (Pu): {Pu:.2f} seconds")


       # for row in pitch_data:
           # write_to_csv(row, 'output.csv')
        
        time.sleep(dt)

except KeyboardInterrupt:
    motor(False,0)
    print ('Socket is now closing')
    #conn.close()
    pi.stop()
