#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, OUTPUT_C, OUTPUT_B, OUTPUT_D, OUTPUT_A, SpeedDPS, MoveTank, MoveSteering, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import LightSensor
from ev3dev2.button import Button
from time import sleep
import sys, os
from math import isnan

#Set up
btn = Button()
LLight = LightSensor(INPUT_1)
RLight = LightSensor(INPUT_4)
drive = MoveTank(OUTPUT_D,OUTPUT_A)
steer = MoveSteering(OUTPUT_D,OUTPUT_A)
os.system('setfont Lat15-TerminusBold14')
speed = 5

def sensordata():
        print("Left Light Sensor: ", end = "", file = sys.stderr)
        print(LLight.reflected_light_intensity, end = " ", file = sys.stderr)
        print("Right Light Sensor: ", end = "", file = sys.stderr)
        print(RLight.reflected_light_intensity, file = sys.stderr)
        
def run(speed):
    turn = 1
    kp = 1
    ki = 0
    kd = 0
    integral = 0
    perror = error = 0
    ## We turn when left and right both register black, 
    while not btn.any():
        lv = LLight.reflected_light_intensity
        rv = RLight.reflected_light_intensity
        print(rv)
        error = rv - lv
        integral += integral + error
        derivative = lv - perror
        # intersections = 0
        piderror = (error * kp) + (integral * ki) + (derivative * kd)
        # piderror = 0 if isnan(piderror) else piderror
        # if abs(piderror) >= 10:
        #     drive.off()
        #     while not lv >= 68:
        #         steer.on(steering = 10, speed = speed)
        if speed + abs(piderror) > 100:
            if piderror >= 0:
                piderror = 100 - speed
            else:
                piderror = speed - 100 
        if (abs(piderror) >= 10) and (turn==1):
            drive.off()
            drive.on_for_seconds(left_speed=0, right_speed=10, seconds=2)
            drive.on_for_seconds(left_speed=5,right_speed=5,seconds=1.3)
            while (rv > 60):
                print("TURNING",file =sys.stderr)
                rv = RLight.reflected_light_intensity
                drive.on(left_speed=0, right_speed=10)
                turn = 0
            

        drive.on(left_speed = speed - piderror, right_speed= speed + piderror)
        sleep(0.01)
        perror = error
        
        
        # print("The P error is:", end = " ", file = sys.stderr)
        # print(piderror, end = " ", file = sys.stderr)
        # print("Left Light Sensor:", end = " ", file = sys.stderr)
        
        # if abs(piderror) >= 10:
        #     print(LLight.reflected_light_intensity, end = " ", file = sys.stderr)
        #     print("Intersection!", file = sys.stderr)
        # else:
        #     print(LLight.reflected_light_intensity, file = sys.stderr)


while not btn.any(): # Until we can get reliable bounds on our sensor data this stays, but we'll replace with try/except in final build
    sensordata()

# run(speed)
