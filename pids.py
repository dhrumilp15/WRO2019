#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_C, OUTPUT_B, OUTPUT_D, OUTPUT_A, SpeedDPS, MoveTank, MoveSteering, SpeedPercent, SpeedDPS
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import LightSensor, ColorSensor
from ev3dev2.button import Button
from time import sleep
import sys, os
import math

btn  = Button()
LLight = LightSensor(INPUT_1)
RLight = LightSensor(INPUT_4)
drive = MoveTank(OUTPUT_B,OUTPUT_C)
os.system('setfont Lat15-TerminusBold14')
speed = 15
kp = 1.25
kd = 0
ki = 0
integral = 0
perror = error = 0
piderror = 0
while not btn.any(): 
    lv = LLight.reflected_light_intensity
    rv = RLight.reflected_light_intensity
    error = round(rv,5) - round(lv,5)
    integral += error
    derivative = error - perror

    piderror = (error * kp) + (integral * ki) + (derivative * kd)
    
    if math.isnan(piderror): # Need to figure out how to better handle NaNs
    	piderror = perror

    if speed + abs(piderror) > 100:
        if piderror >= 0:
            piderror = 100 - speed
        else:
            piderror = speed - 100

    drive.on(left_speed = speed - piderror, right_speed= speed + piderror)
	#sleep(0.01) for debugging purposes, causes errors as robot can't update values when in sleep()
    perror = error