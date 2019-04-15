#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_C, OUTPUT_B, OUTPUT_D, OUTPUT_A, SpeedDPS, MoveTank, MoveSteering, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import LightSensor
from ev3dev2.button import Button
from time import sleep
import sys, os

btn = Button()
LLight = LightSensor(INPUT_1)
RLight = LightSensor(INPUT_4)
drive = MoveTank(OUTPUT_A,OUTPUT_D)
steer = MoveSteering(OUTPUT_A,OUTPUT_D)
os.system('setfont Lat15-TerminusBold14')
speed = 20

def sensordata():
        print("Left Light Sensor: ", end = "", file = sys.stderr)
        print(LLight.reflected_light_intensity, end = " ", file = sys.stderr)
        print("Right Light Sensor: ", end = "", file = sys.stderr)
        print(RLight.reflected_light_intensity, file = sys.stderr)

def turn(direc):
    lv = LLight.reflected_light_intensity
    rv = RLight.reflected_light_intensity
    if direc == "L" or direc == "l":
        while rv > 50:
            rv = RLight.reflected_light_intensity
            drive.on(left_speed=0, right_speed=10)
            sleep(0.01)
    elif direc == "R" or direc == "r":
        while lv > 50:
            lv = LLight.reflected_light_intensity
            drive.on(left_speed=10, right_speed=0)
            sleep(0.01)

def linefollower(speed):
    kp = 1
    ki = 0
    kd = 0
    integral = 0
    perror = error = 0    
    while not btn.any():
        lv = LLight.reflected_light_intensity
        rv = RLight.reflected_light_intensity
        sensordata()
        
        error = rv - lv

        integral += integral + error
        derivative = lv - perror

        piderror = (error * kp) + (integral * ki) + (derivative * kd)
        if speed + abs(piderror) > 100:
            if piderror >= 0:
                piderror = 100 - speed
            else:
                piderror = speed - 100
            
        drive.on(left_speed = speed - piderror, right_speed= speed + piderror)
        sleep(0.01)
        perror = error
        
        print("The P error is:", end = " ", file = sys.stderr)
        print(piderror, end = " ", file = sys.stderr)
    
    def dti(n):
        intersections = 0
        while intersections != n-1:
            
            intersections += 1
def main():
    linefollower(speed)

if __name__ == "__main__":
    main()

"""
Placed directly in front of top front line
dti
Drive by up to first intersection, store coloured bricks into orientation list
turn left
drive to 5th intersection (4 intersections have passed)
turn left
drive up and slightly past first intersection (cs is on half-line of robot)
Is np black?
    Y:
        Back up until at intersection
        Turn right
        Drive forward and overshoot position
        Pick up bnp
        Full 180
        Drive past intersection to red zone to place
        Orient claw in red position
        Drop bnp
        Back up
        Reorient Claw to accept a new bnp
Similar process for blue part
.
. Place first two BNP in position (with center point at mid of np)
.
Full 180
Drive to intersection
turn left
drive to intersection
turn right
dti
turn right
drive to "second" intersection
.
. Place last two BNP in positions (with center point at mid of np)
.
full 180
dti
turn left
drive up to 4th intersection
turn left
dti
turn right
Reset claw to forward-facing
Overshoot and pick up FIBER OPTIC CABLE
full 180
dti
turn left
dti
turn right
dti
turn right
drive to second intersection
turn left
drive up to when can't see balck / hardcode
hardcode distance to position to deposit FIBER OPTIC CABLE
reverse
get back on line (rotating until sees line, etc.)
dti
turn left
drive to 2nd intersection ( 1 intersection passed)
turn right
dti
turn right
dti
turn left
reset claw to forward facing
overshoot and pick up FIBER OPTIC CABLE
full 180
dti
turn right
dti
turn left
drive to 5th intersection ( 4 intersections passed)
turn left
drive to second intersection (1 intersection passed)
turn left
drive up to when can't see balck / hardcode
hardcode distance to position to deposit FIBER OPTIC CABLE
reverse
get back on line (rotating until sees line, etc.)
dti
turn right
drive to second intersection (1 intersection passed)
turn left
drive hardcode to finish
"""
