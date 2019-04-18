#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_C, OUTPUT_B, OUTPUT_D, OUTPUT_A, SpeedDPS, MoveTank, MoveSteering, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import LightSensor, ColorSensor
from ev3dev2.button import Button
from time import sleep
import sys, os

btn = Button()

LLight = LightSensor(INPUT_1)
RLight = LightSensor(INPUT_4)
cs = ColorSensor()

drive = MoveTank(OUTPUT_A,OUTPUT_D)
steer = MoveSteering(OUTPUT_A,OUTPUT_D)

os.system('setfont Lat15-TerminusBold14')

speed = 10
orient = {'N': "1",
          'E': "1",
          'S': "1",
          'W': "1"}

def sensordata():
        print("Left Light Sensor: ", end = "", file = sys.stderr)
        print(LLight.reflected_light_intensity, end = " ", file = sys.stderr)
        print("Right Light Sensor: ", end = "", file = sys.stderr)
        print(RLight.reflected_light_intensity, file = sys.stderr)

def turn(direc): # Tune so that we position ourselves properly on the line
    lv = LLight.reflected_light_intensity
    rv = RLight.reflected_light_intensity
    if direc == "L" or direc == "l":
        drive.on_for_degrees(-speed, speed, 10)
        while rv > 50:
            drive.on(left_speed=0, right_speed=10)
    elif direc == "R" or direc == "r":
        while lv > 50:
            lv = LLight.reflected_light_intensity
            drive.on(left_speed=10, right_speed=0)
            sleep(0.01)
    drive.off()

def dti(speed, n, kp): # Drive to nth intersection
    kp = kp
    ki = 0
    kd = 0
    integral = 0
    perror = error = 0
    inters = 0
    piderror = 0
    while not btn.any(): # Remember to try stuff twice, this is a keyboard interrupt
        lv = LLight.reflected_light_intensity
        rv = RLight.reflected_light_intensity
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
        
        # Drive up to nth intersection
        if lv <= 50 and rv <= 55: # Currently at an intersection 
            if inters == n: # Currently at nth intersection
                drive.off()
                return
            drive.off()
            drive.on_for_degrees(speed, speed, 20) 
            inters += 1

        print("Left Value: {}, Right Value: {}, P error: {}, Intersections: {}".format(lv, rv, piderror, inters), file=sys.stderr)

def assigncolours(speed):
    kp = 0.5
    ki = 0
    kd = 0
    integral = 0
    perror = error = 0
    piderror = 0
    while not btn.any(): # Remember to try stuff twice, this is a keyboard interrupt
        lv = LLight.reflected_light_intensity
        rv = RLight.reflected_light_intensity
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
        print(cs.color, file = sys.stderr)
        
        if cs.color != cs.COLOR_NOCOLOR and cs.color in [cs.COLOR_RED, cs.COLOR_GREEN, cs.COLOR_YELLOW, cs.COLOR_BLUE]:
            if orient["E"] == "1":
                orient["E"] = cs.color
                eastcolour = cs.color
                while cs.color == eastcolour:
                    drive.on(10,10)
            else:
                if orient["S"] == "1":
                    orient["S"] = cs.color
                    drive.on_for_degrees(speed, speed, degrees=40)
                    southcolour = cs.color
                    while cs.color == southcolour:
                        drive.on(10,10)
                else:
                    if orient["W"] == "1":
                        orient["W"] = cs.color
                        drive.on_for_degrees(speed, speed, degrees=40)
                        westcolour = cs.color
                        while cs.color == westcolour:
                            drive.on(10,10)
                    else:
                        if orient["N"] == "1":
                            orient["N"] = cs.color
                            drive.on_for_degrees(speed, speed, degrees=40)
                            northcolour = cs.color
                            while cs.color == northcolour:
                                drive.on(10,10)
        if lv <= 50 and rv >= 55:
            drive.off()
            return

def main():
    # while not btn.any():
    #     sensordata()
    ## STORING COLOURS
    # drive.on_for_degrees(left_speed=speed, right_speed=speed, degrees=50) # To drive past little initial intersection
    # assigncolours(speed)
    # print(orient, file = sys.stderr)
    turn("L")

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
