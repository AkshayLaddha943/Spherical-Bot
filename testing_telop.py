# Servo Control
import time
import pigpio
import socket
import sys
import board
import busio
import adafruit_bno055
import math

# Use these lines for I2C IMU feedback
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)


#Setting up pwm for servo
pi =  pigpio.pi()                    
pi.set_mode(22, pigpio.OUTPUT)
pi.set_mode(23, pigpio.OUTPUT)


#  Setting up the N20 motor  
#pi.setmode(GPIO_ pin number, IN/OUT)

pi.set_mode(13,pigpio.OUTPUT)  #PWMA 13        7
pi.set_mode(17,pigpio.OUTPUT)  #AIN2 17       11
pi.set_mode(18,pigpio.OUTPUT)  #AIN1 18        12
pi.set_mode(27,pigpio.OUTPUT)  #STBY 27        13

global roll_actual

def set_servo_dutycycle(value):
    pi.set_servo_pulsewidth(22, value)
    pi.set_servo_pulsewidth(23, value)


def map(value, axes_min, axes_max, actuate_min, actuate_max):
    axes_span = axes_max-axes_min
    actuate_span = actuate_max-actuate_min
    value_scaled = (float(value - axes_min)/float(axes_span))
    return int(actuate_min+(value_scaled*actuate_span))


def front_servo(angle):


    #angle here is negated because its in opposite direction facing
    pulse_width = map(-angle, -90, 90, 1000, 2000) 
    pi.set_servo_pulsewidth(22, pulse_width)

def rear_servo(angle):

    pulse_width = map(angle, -90, 90, 1000, 2000)
    pi.set_servo_pulsewidth(23, pulse_width)


def get_pitch():
	yaw, roll, pitch = sensor.euler
	print('Im geting pitch ', pitch)
	return pitch

def pitch_control(set_pt, actual_pitch, Kp_pitch, pitch_err, user_pwm):
    pwm = max(0, min(200, 140 * Kp_pitch * pitch_err + user_pwm))
    return pwm

def roll_control():
	Kp = 1
	P = Kp*roll_err
	front_servo(P)
	rear_servo(P)
	print('Im in roll controller P ',P) 

def forward_ascent():
	for pwm_a in range(mot_pwm,0, -5):
		motor(True, pwm_a)
		time.sleep(0.05)




def backward_descent():
	for pwm_b in range(mot_pwm,0, -5):
		motor(False, pwm_b)
		time.sleep(0.05)



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


#Setting up Servo for Android control
HOST = ''
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
mot_dir = True
Kp_pitch = 0.00876
set_pt_pitch = 0.0 

while True:
    data=conn.recv(1024)

    if not data: break
    
    pos_b = data.rfind(b'b')
    data =  data[:pos_b]
    pos_a = data.rfind(b'a')
    data = data[pos_a+1:]
    pos_y = bytes.find(data , b'y')

    pos_p = data.rfind(b'p')

    str_x = data[1:pos_y]
    str_y = data[pos_y+1:pos_p]
    str_p = data[pos_p+1:]

    ###############################################################


    x = int(str_x)-50
    y=  int(str_y)-50
    #print(data)
    p = int(str_p)-10
    # p = 10
    #print(p)
    #print(str_x, str_y, str_p)
    print(x,y,p)
    set_servo_dutycycle(1500)
    servo_angle = map(p,20,80,-90,90)
    front_servo(servo_angle)
    rear_servo(servo_angle)
    #print(servo_angle)


    pitch_actual = get_pitch()
    pitch_err = (set_pt_pitch - pitch_actual)
    #print(x,y,p)


    if x == 0 and y == 0:
        
        if flag_run == True and mot_dir == True:

            forward_ascent()
            flag_run=False

        elif flag_run == True and mot_dir == False:
            backward_descent()
            flag_run = False
        
        pwm = 128
        mot_pwm = pitch_control(set_pt_pitch, pitch_actual, Kp_pitch, pitch_err, pwm)
        mot_dir = False
        motor(mot_dir, mot_pwm)


     #pos_a != -1 and pos_b !=-1 and pos_a < pos_b


    
    elif (pos_a != -1 and pos_b !=-1 and pos_a < pos_b):
        

        if y>0:
            mot_pwm = map(y,0,65, 0, 200)
            mot_dir = True
            #print(mot_pwm)
            motor(mot_dir, mot_pwm)
            flag_run = True
    


        else:
            mot_pwm = map(abs(y),0,65, 0, 200)
            mot_dir = False
            #print(mot_pwm)
            motor(mot_dir, mot_pwm)
            flag_run = True

    


    else:
    	print('In else')
    
    
      


print ('Socket is now closing')
conn.close()
pi.stop()
