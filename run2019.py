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

linter, rinter = 0,0

os.system('setfont Lat15-TerminusBold14')

def calibratelights(lbline, lbblack, lbwhite, rbblack, rbwhite):
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
    
    print("Right Sensor Black: ")
    while not btn.any():
        rbblack = int(RLight.reflected_light_intensity)
    print(rbblack, file = sys.stderr)

def sensordata():
        print("Left Light Sensor: ", end = "", file = sys.stderr)
        print(LLight.reflected_light_intensity, end = " ", file = sys.stderr)
        print("Right Light Sensor: ", end = "", file = sys.stderr)
        print(RLight.reflected_light_intensity, file = sys.stderr)

speed = 10
        
def run(speed):
    kp = 1
    ki = 0
    kd = 0
    integral = 0
    perror = error = 0
    ## We turn when left and right both register black, 
    while not btn.any():
        lv = LLight.reflected_light_intensity
        rv = RLight.reflected_light_intensity

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
        
        # if abs(piderror) >= 10:
        #     drive.off()
        #     steer.on_for_degrees(steering = -100, speed = speed, degrees = 50)

        drive.on(left_speed = speed - piderror, right_speed= speed + piderror)
        sleep(0.01)
        perror = error
        # if lv < 50 and rv < 50: # if both register black, which means you're at an intersection
        #     steer.on_for_seconds(
        #         steering = -100,
        #         speed = speed,
        #         seconds = 0.1
        #     )
        #     # while not rv < 50:
        #     #     steer.on(steering=-100, speed=speed)
        #     #     sleep(0.01)
        #     # if intersections == 4:
        #     #     steer.on_for_degrees(steering=-100, speed=speed, degrees=75)
        #     #     sleep(0.01)
        #     # else:
        #     #     intersections += 1
        # else:
        #     piderror = (error * kp) + (integral * ki) + (derivative * kd)

        #     if speed + abs(piderror) > 100:
        #         if piderror >= 0:
        #             piderror = 100 - speed
        #         else:
        #             piderror = speed - 100

        #     drive.on(left_speed = speed - piderror, right_speed= speed + piderror)
        #     sleep(0.01)
        #     perror = error
        
        print("The P error is:", end = " ", file = sys.stderr)
        print(piderror, end = " ", file = sys.stderr)
        print("Left Light Sensor:", end = " ", file = sys.stderr)
        
        if abs(piderror) >= 10:
            print(LLight.reflected_light_intensity, end = " ", file = sys.stderr)
            print("Intersection!", file = sys.stderr)
        else:
            print(LLight.reflected_light_intensity, file = sys.stderr)


# while not btn.any(): # Until we can get reliable bounds on our sensor data this stays, but we'll replace with try/except in final build
#     sensordata()

run(speed)

def main():
    
    run(speed)
    # left()
    # right()
    run(speed)


if __name__ == "__main__":
    main()
"""
Left

White: 74.1 - 76
Black: < 55
Half: 56 - 69

Right

White: > 67
Black: < 47
"""
