# Spherical-Bot

This repository encapsulates the information related to board dimensions, electronics, sensors and its testing scripts, to controller node for the development of Spherical Bot 2.0

## Table of Contents

* [Hardware](https://github.com/AkshayLaddha943/Spherical-Bot?tab=readme-ov-file#hardware)
  * [Hardware Requirement](#hardware-requirements)
  * [PCB Dimensions](#pcb-dimensions)
* [Software](https://github.com/AkshayLaddha943/Spherical-Bot?tab=readme-ov-file#software)
  * [Software Pre-Requisites](#software-pre-requisites)
  * [IMU Test](#imu-test)
  * [Picamera Test](#picamera-test)
  * [Forward Motion](#forward-motion)
* [Control](https://github.com/AkshayLaddha943/Arrow_SensorFusion_turtlebot3_ws#installing-required-rosdep-packages-and-dependencies)
  * [Pitch Control](#software-installation)
  * [Roll Control](#software-configuration)


# Hardware

## Hardware Requirement


<p align="center"> <img src="https://github.com/AkshayLaddha943/Spherical-Bot/blob/main/imgs/hardware.PNG" height="700" width="500" alt="Final BOM">
<br/>


## PCB Dimensions

<p align="center"> <img src="https://github.com/AkshayLaddha943/Spherical-Bot/blob/main/imgs/pcb_dim.PNG" height="300" width="300" alt="Overall Board Dimensions">
<br/>

<p align="center"><img src="https://github.com/AkshayLaddha943/Spherical-Bot/blob/main/imgs/pcb_measure.PNG" height="300" width="300" alt="PCB Dim" hspace="10">
<img src="https://github.com/AkshayLaddha943/Spherical-Bot/blob/main/imgs/bom_final.PNG" height="300" width="300" alt="Final BOM">


# Software

## Software Pre-Requisites

1. Clone the Spherical-Bot repository
2. Install all the required dependencies -> 
```
pip install -r requirements.txt
```

3. Run the scripts

## IMU Test

The IMU being used is the Bosch 9-axis BNO-055 sensor -

<p align="center"> <img src="https://github.com/AkshayLaddha943/Spherical-Bot/blob/main/imgs/bno_055_imu.jpg" height="300" width="300" alt="BNO_IMU">
<br/>

### Plotting the IMU result

<p align="center"><img src="https://github.com/AkshayLaddha943/Spherical-Bot/blob/main/imgs/imu.PNG" height="300" width="300" alt="IMU_command_line" hspace="10">
<img src="https://github.com/AkshayLaddha943/Spherical-Bot/blob/main/imgs/rpy_updated.PNG" height="300" width="300" alt="IMU_graph">

### To test the IMU output - 

1. Navigate to sensor_tests/IMU_test directory
2. Run the test_imu.py


## PiCamera Test

The Camera being used is the Waveshare OV5647 220FOV Camera -

<p align="center"> <img src="https://github.com/AkshayLaddha943/Spherical-Bot/blob/main/imgs/ov5647.PNG" height="300" width="300" alt="Camera">
<br/>

### Viewing the output from camera

<p align="center"><img src="https://github.com/AkshayLaddha943/Spherical-Bot/blob/main/imgs/picamera_view.jpg" height="300" width="300" alt="Cam_output" hspace="10">
<img src="https://github.com/AkshayLaddha943/Spherical-Bot/blob/main/imgs/picam_opencv.PNG" height="300" width="300" alt="Cam_fw_output">

### To test the camera output - 

1. Note down the system's IP
2. Navigate to sensor_tests/Picamera_test directory
3. Run the test_picam2.py
4. Head to the following page - http://{IP_ADDRESS}:8000/index.html


## Forward Motion

## Moving the robot forward

The following clip shows the robot's forward movement - 

https://github.com/user-attachments/assets/5aabcf7d-3285-4010-ae62-a8122f7702a7


The 


https://github.com/user-attachments/assets/51d89cce-b28e-4baa-b23c-206a33709b13



### To test the camera output - 

1. Note down the system's IP
2. Navigate to sensor_tests/Picamera_test directory
3. Run the test_picam2.py
4. Head to the following page - http://{IP_ADDRESS}:8000/index.html


# Control

## Pitch Control

### Methodology
The pitch control of the Spherical Bot is managed using a Proportional Controller (P-controller). The control strategy is implemented to maintain the desired pitch angle by adjusting the servo motors and the N20 motor based on the feedback from the IMU sensor.

### Mathematical formula

The Proportional Control equation used is:

$$
P_{\text{error}} = \text{Set Point} - \text{Actual Pitch}
$$

$$
\text{Motor PWM} = \max(0, \min(200, K_p \times P_{\text{error}} + \text{User PWM}))
$$

where:
-  \( P_{\text{error}} \) is the pitch error.
- $$ \( \text{Set Point} \) is the desired pitch angle (set to 0.0 degrees in this case).
- $$ \( \text{Actual Pitch} \) is the current pitch angle measured by the IMU sensor.
- $$ \( K_p \) is the proportional gain, set to 0.00876.
- $$ \( \text{User PWM} \) is a constant value (set to 185) that provides the base motor speed.
- $$ \( \text{Motor PWM} \) is the calculated PWM value to drive the motor, ensuring it stays within the range of 0 to 200

### Optimal Value

The optimal proportional gain $$ (\( K_p \)) for achieving stable pitch control is determined to be:

$$ \[ K_p = 0.00876 \]


## Roll Control

### Methodology

The roll control of the Spherical Bot is managed using a Proportional Controller (P-controller). The control strategy is implemented to maintain the desired roll angle by adjusting the servo motors and the N20 motor based on feedback from the IMU sensor.

### Mathematical Formula

The Proportional Control equation used is:

$$ R_{\text{error}} = \text{Set Point} - \text{Actual Roll} 

$$ \text{Motor PWM} = \max(0, \min(200, K_p \times R_{\text{error}} + \text{User PWM})) 

where:
- \( R_{\text{error}} \) is the roll error.
- \( \text{Set Point} \) is the desired roll angle (set to 0.0 degrees in this case).
- \( \text{Actual Roll} \) is the current roll angle measured by the IMU sensor.
- \( K_p \) is the proportional gain, set to 0.00876.
- \( \text{User PWM} \) is a constant value (set to 185) that provides the base motor speed.
- \( \text{Motor PWM} \) is the calculated PWM value to drive the motor, ensuring it stays within the range of 0 to 200.

### Optimal Value

The optimal proportional gain (\( K_p \)) for achieving stable roll control is determined to be:

\[ K_p = 0.00876 \]

This value ensures that the Spherical Bot maintains the desired roll angle with minimal oscillation and quick response to changes in roll
