#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_C, OUTPUT_B, SpeedDPS, MoveTank, MoveSteering, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import LightSensor
from ev3dev2.button import Button
from time import sleep
import sys, os

#Set up
btn = Button()
LLight = LightSensor(INPUT_2)
RLight = LightSensor(INPUT_3)

drive = MoveTank(OUTPUT_B,OUTPUT_C)
steer = MoveSteering(OUTPUT_B,OUTPUT_C)

lbline, lbblack, lbwhite = 58.9, 0, 0
rbline, rbblack, rbwhite = 0, 0, 0

minRef = 40.4
maxRef = 65.9
os.system('setfont Lat15-TerminusBold14')

def calibratelights(lbline, lbblack, lbwhite, rbline, rbblack, rbwhite):
    print("Left Sensor White: ")
    while not btn.any():
        lbwhite = int(LLight.reflected_light_intensity)
    print(lbwhite, file = sys.stderr)
    
    print("Left Sensor Line: ")
    while not btn.any():
        lbline = int(LLight.reflected_light_intensity)
    print(lbline, file = sys.stderr)
    
    print("Left Sensor Black: ")
    while not btn.any():
        lbblack = int(LLight.reflected_light_intensity)
    print(lbblack, file = sys.stderr)
    
    print("Right Sensor White: ")
    while not btn.any():
        rbwhite = int(RLight.reflected_light_intensity)
    print(rbwhite, file = sys.stderr)
    
    print("Right Sensor Line: ")
    while not btn.any():
        rbline = int(RLight.reflected_light_intensity)
    print(rbline, file = sys.stderr)
    
    print("Right Sensor Black: ")
    while not btn.any():
        rbblack = int(RLight.reflected_light_intensity)
    print(rbblack, file = sys.stderr)

def sensordata():
        print("Left Light Sensor: ", end = "", file = sys.stderr)
        print(LLight.reflected_light_intensity, end = " ", file = sys.stderr)
        print("Right Light Sensor: ", end = "", file = sys.stderr)
        print(RLight.reflected_light_intensity, file = sys.stderr)

speed = 40

def calcsteering(piderror, power):
    if piderror >= 0:
        if piderror > 100:
            leftpower = 0
            rightpower = power
        else:
            leftpower = power - ((power*piderror) / 100)
            rightpower = power
    else:
        if piderror < -100:
            leftpower = power
            rightpower = 0
        else:
            leftpower = power
            rightpower = power - ((power*piderror) / 100)
    return (leftpower, rightpower)
        
def run(lbline, speed, maxRef, minRef): # lbline is the target value
    kp = 1
    ki = 0
    kd = 0
    integral = 0
    perror = error = 0
    while not btn.any():
        lv = LLight.reflected_light_intensity
        # error = lbline - (100 * (lv - minRef) / (maxRef - minRef))
        error = lbline - lv
        integral = 0.5 * integral + error # Not sure why the guy multiplies integral by 1/2, but going to keep it like this until I figure it out
        derivative = lv - perror

        piderror = ((error * kp) + (integral * ki) + (derivative * kd))

        if speed + abs(piderror) > 100:
            if piderror >= 0:
                piderror = 100 - speed
            else:
                piderror = speed - 100

            drive.on_for_seconds(left_speed = speed - piderror, right_speed= speed + piderror, seconds = 0.5)
        sleep(0.01)
        
        print("The P error is:", end = " ", file = sys.stderr)
        print(piderror, end = " ", file = sys.stderr)
        print("Left Light Sensor:", end = " ", file = sys.stderr)
        print(LLight.reflected_light_intensity, file = sys.stderr)
        
        perror = error

# while not btn.any(): # Until we can get reliable bounds on our sensor data this stays, but we'll replace with try/except in final build
#     sensordata()

run(lbline,speed,maxRef, minRef)


"""
Left

White: 74.1 - 76
Black: < 55
Half: 56 - 69

Right

White: > 67
Black: < 47
"""
