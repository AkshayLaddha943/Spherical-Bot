# Servo Control
import time
import pigpio
import socket
import sys
import RPi.GPIO as GPIO

#Setting up pwm for servo
pi =  pigpio.pi()                    
pi.set_mode(22, pigpio.OUTPUT)
pi.set_mode(23, pigpio.OUTPUT)


#  Setting up the N20 motor   pi.setmode(GPIO_ pin number, IN/OUT)

pi.set_mode(13,pigpio.OUTPUT)  #PWMA 13         7
pi.set_mode(17,pigpio.OUTPUT)  #AIN2 17       11
pi.set_mode(18,pigpio.OUTPUT)  #AIN1 18        12
pi.set_mode(27,pigpio.OUTPUT)  #STBY 27        13


def map(value, axes_min, axes_max, actuate_min, actuate_max):
    axes_span = axes_max-axes_min
    actuate_span = actuate_max-actuate_min
    value_scaled = (float(value - axes_min)/float(axes_span))
    return int(actuate_min+(value_scaled*actuate_span))


def front_servo(angle):

    pulse_width = map(angle, -30, 30, 1300, 1900)
    pi.set_servo_pulsewidth(22, pulse_width)

def rear_servo(angle):

    pulse_width = map(angle, -30, 30, 1100, 1700)
    pi.set_servo_pulsewidth(23, pulse_width)


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


while True:
    data=conn.recv(1024)
    v = 0
    p = 0
    if not data: break
    
    pos_b = data.rfind('b')
    data =  data[:pos_b]
    pos_a = data.rfind('a')
    data = data[pos_a+1:]
    pos_y = str.find(data , 'y')

    if (pos_a != -1 and pos_b !=-1 and pos_a < pos_b):
        str_x = data[1:pos_y]
        str_y = data[pos_y+1:]

        x = int(str_x)-50
        y=  int(str_y)-50

        servo_angle = map(x,-65,65,-30,30)

        front_servo(-servo_angle)
        rear_servo(servo_angle)

        if y>0:
            mot_pwm = map(y,-65,65, 30, 100)
            mot_dir = True
            motor(mot_dir, mot_pwm)
        


        elif y<0:
            mot_pwm = map(y,65,-65, 30, 100)
            mot_dir = False
            motor(mot_dir, mot_pwm)

        

        else:
            mot_pwm = 0
            mot_dir = True
            motor(mot_dir, mot_pwm)


        






            
    else:
        print("Else is running")


print ('Socket is now closing')
conn.close()
pi.stop()
