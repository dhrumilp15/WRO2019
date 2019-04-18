#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_C, OUTPUT_B, OUTPUT_D, OUTPUT_A, SpeedDPS, MoveTank, MoveSteering, SpeedPercent, SpeedDPS
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import LightSensor, ColorSensor
from ev3dev2.button import Button
from time import sleep
import sys, os

"""
CHANGE
- Light sensor bounds
- Tune PID
- Tune Turning
"""
btn = Button()

LLight = LightSensor(INPUT_1)
RLight = LightSensor(INPUT_4)
cs = ColorSensor()

drive = MoveTank(OUTPUT_A,OUTPUT_D)
steer = MoveSteering(OUTPUT_A,OUTPUT_D)
heightmotor = LargeMotor(OUTPUT_B)
clawactuator = MediumMotor(OUTPUT_C)

os.system('setfont Lat15-TerminusBold14')

speed = 20
orient = {'N': "1",
          'E': "1",
          'S': "1",
          'W': "1"}

def sensordata():
        print("Left Light Sensor: ", end = "", file = sys.stderr)
        print(LLight.reflected_light_intensity, end = " ", file = sys.stderr)
        print("Right Light Sensor: ", end = "", file = sys.stderr)
        print(RLight.reflected_light_intensity, file = sys.stderr)

def turn(direc):
    drive.on_for_degrees(SpeedDPS(40),SpeedDPS(40),40)
    if direc == "L" or direc == "l":
        steer.on_for_degrees(steering=-100, speed=SpeedDPS(360), degrees=1050)
    elif direc == "R" or direc == "r":
        steer.on_for_degrees(steering=100, speed=SpeedDPS(360), degrees=1050)
    steer.off()

# EXPERIMENTAL - WILL OPTIMIZE CODE IF NECESSARY LATER
def followline(speed, colourmode = False, intersectionmode = False, intersmax = 0): # OPTIMIZING PID CODE, hehe what a brilliant time amirite or amirite
    kp = 1
    ki = 0
    kd = 0
    integral = 0
    perror = error = 0
    inters = 0
    piderror = 0
    while not btn.any(): # Remember to try stuff twice, this is a keyboard interrupt
        # BASIC PID
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

        # COLOUR ASSIGNMENT MODE
        if colourmode == True:
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
        # INTERSECTION MODE
        if intersectionmode == true:
            if lv <= 50 and rv <= 55: # Currently at an intersection 
                if inters == intersmax: # Currently at nth intersection
                    drive.off()
                    return
                drive.off()
                drive.on_for_degrees(speed, speed, 20) 
                inters += 1

def dti(speed, n): # Drive to nth intersection
    kp = 1.1
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
        # These values are subject to change depending on outside factors, CHANGE ON COMPETITION DAY
        if (lv <= 50 and rv <= 55) or (lv <= 50 and rv >= 55) or (lv >= 50 and rv <= 55): # Currently at an intersection
            inters += 1
            if inters == n: # Currently at nth intersection
                drive.off()
                return
            drive.off()
            drive.on_for_seconds(SpeedDPS(115), SpeedDPS(115), 1) 

        print("Left Value: {}, Right Value: {}, P error: {}, Inters: {}".format(lv, rv, piderror, inters), file=sys.stderr)

def assigncolours(speed): # Does beginning, up to first intersection
    kp = 1
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

def firstbnps(speed):
    kp = 1
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
        
        # COLOUR CASES
        if cs.color == cs.COLOR_BLACK:
            drive.off()
            redpos = ""
            for pos, colour in orient.items():
                if colour == cs.COLOR_RED:
                    redpos = pos
            if redpos in ["S", "W"]: # Forward - pickup
                #Pick it up
                turn("R")
                drive.on_for_degrees(SpeedDPS(360), SpeedDPS(360), 100) # Overshoot
                heightmotor.on_for_degrees(speed=300, degrees=-20)


def main():
    heightmotor.on(speed=speed)
    heightmotor.wait_until_not_moving()
    # while not btn.any():
    #     sensordata()
    ## STORING COLOURS
    # drive.on_for_degrees(left_speed=speed, right_speed=speed, degrees=50) # To drive past little initial intersection
    # assigncolours(speed)
    # print(orient, file = sys.stderr) #DEBUG
    # GO TO FIRST BNPs
    dti(speed, 2)
    turn("L")
    dti(speed, 1)
    #firstbnps(speed)


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
